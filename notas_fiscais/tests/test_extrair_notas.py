"""Testes unitários para extrair_notas.py."""

import base64
import gzip
import json
import os
import tempfile
from unittest.mock import MagicMock, patch, mock_open

import pytest

import extrair_notas as en

# === Helpers ===

NS_DECL = 'xmlns="http://www.sped.fazenda.gov.br/nfse"'


def _build_xml(nnfse="100", dcompet="2026-02-15", dhemi="2026-02-15T10:00:00",
               dhproc="2026-02-16T08:00:00", vserv="200.00", xdesc=""):
    """Constrói um XML NFS-e mínimo."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<NFSe {NS_DECL}>
  <infNFSe>
    <nNFSe>{nnfse}</nNFSe>
    <dCompet>{dcompet}</dCompet>
    <dhEmi>{dhemi}</dhEmi>
    <dhProc>{dhproc}</dhProc>
    <valores>
      <vServ>{vserv}</vServ>
    </valores>
    <xDescServ>{xdesc}</xDescServ>
  </infNFSe>
</NFSe>"""


def _build_doc(xml_str, chave="CHAVE123", nsu=1):
    """Simula um doc da API: XML compactado em GZip + Base64."""
    xml_bytes = xml_str.encode("utf-8")
    compressed = gzip.compress(xml_bytes)
    b64 = base64.b64encode(compressed).decode("ascii")
    return {"ArquivoXml": b64, "ChaveAcesso": chave, "NSU": nsu, "TipoDocumento": "NFSE"}


# === Testes formatar_cnpj ===

class TestFormatarCnpj:
    def test_14_digitos(self):
        assert en.formatar_cnpj("09223558000100") == "09.223.558/0001-00"

    def test_menos_de_14_digitos_zfill(self):
        assert en.formatar_cnpj("9223558000100") == "09.223.558/0001-00"

    def test_outro_cnpj(self):
        assert en.formatar_cnpj("12345678000199") == "12.345.678/0001-99"


# === Testes formatar_data_br ===

class TestFormatarDataBr:
    def test_data_iso(self):
        assert en.formatar_data_br("2026-02-15") == "15/02/2026"

    def test_data_com_hora(self):
        assert en.formatar_data_br("2026-02-15T10:30:00") == "15/02/2026"

    def test_data_vazia(self):
        assert en.formatar_data_br("") == ""

    def test_data_curta(self):
        assert en.formatar_data_br("2026") == "2026"

    def test_data_none(self):
        assert en.formatar_data_br(None) is None


# === Testes formatar_valor_br ===

class TestFormatarValorBr:
    def test_valor_decimal(self):
        assert en.formatar_valor_br(17.5) == "17,50"

    def test_valor_inteiro(self):
        assert en.formatar_valor_br(100.0) == "100,00"

    def test_valor_zero(self):
        assert en.formatar_valor_br(0.0) == "0,00"

    def test_valor_centavos(self):
        assert en.formatar_valor_br(0.99) == "0,99"


# === Testes decodificar_xml ===

class TestDecodificarXml:
    def test_decodifica_gzip_base64(self):
        xml_original = "<root>teste</root>"
        compressed = gzip.compress(xml_original.encode("utf-8"))
        b64 = base64.b64encode(compressed).decode("ascii")
        assert en.decodificar_xml(b64) == xml_original


# === Testes extrair_dados_nota ===

class TestExtrairDadosNota:
    """Testes para extrair_dados_nota com diferentes formatos de rateio."""

    def test_formato1_com_rateio(self):
        """Formato série 49999: SALAO-PARCEIRO + PROFISSIONAL-PARCEIRO."""
        desc = (
            "SERVIÇO R$ 200,00 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$120,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$80,00"
        )
        xml = _build_xml(nnfse="500", vserv="200.00", xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["nfse"] == "500"
        assert nota["tem_rateio"] is True
        assert "12345678000199" in nota["parceiros"]
        assert nota["parceiros"]["12345678000199"]["cota_parceiro"] == 80.0
        assert nota["parceiros"]["12345678000199"]["cota_salao"] == 120.0

    def test_formato1_sem_rateio(self):
        """Formato série 49999 sem PROFISSIONAL-PARCEIRO: cota 100% salão."""
        desc = (
            "SERVIÇO R$ 200,00 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$200,00"
        )
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is False
        assert nota["parceiros"] == {}

    def test_formato2_com_rateio(self):
        """Formato série 1: Rateio referente a Salao/Profissional parceiro."""
        desc = (
            "Serviço prestado. "
            "Rateio referente a Salao/Profissional parceiro: "
            "CNPJ: 09223558000100 - DEPILAGOS - R$ 150,00 "
            "CNPJ: 98765432000111 - PARCEIRA X - R$ 50,00"
        )
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is True
        assert "98765432000111" in nota["parceiros"]
        assert nota["parceiros"]["98765432000111"]["cota_parceiro"] == 50.0
        assert nota["parceiros"]["98765432000111"]["cota_salao"] == 150.0

    def test_sem_nenhum_texto_rateio(self):
        """Serviço da equipe interna, sem rateio."""
        desc = "Serviço de depilação a laser - sessão completa"
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is False
        assert nota["parceiros"] == {}

    def test_multiplos_parceiros_diferentes(self):
        """Nota com 2 profissionais parceiros diferentes, cota salão dividida proporcionalmente."""
        desc = (
            "SERVIÇO 1 R$ 100 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$60,00 "
            "PROFISSIONAL-PARCEIRO: 11111111000100 COTA-PARTE R$20,00 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$40,00 "
            "PROFISSIONAL-PARCEIRO: 22222222000100 COTA-PARTE R$30,00"
        )
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is True
        assert len(nota["parceiros"]) == 2
        # Cota salão total = 60 + 40 = 100
        # Parceiro 1: 20/(20+30) = 40% → cota salão = 40
        # Parceiro 2: 30/(20+30) = 60% → cota salão = 60
        p1 = nota["parceiros"]["11111111000100"]
        p2 = nota["parceiros"]["22222222000100"]
        assert p1["cota_parceiro"] == 20.0
        assert p2["cota_parceiro"] == 30.0
        assert abs(p1["cota_salao"] - 40.0) < 0.01
        assert abs(p2["cota_salao"] - 60.0) < 0.01

    def test_multiplos_servicos_mesmo_parceiro(self):
        """Vários serviços do mesmo parceiro: cotas somadas em única entrada."""
        desc = (
            "SERVIÇO 1 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$60,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$40,00 "
            "SERVIÇO 2 "
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$30,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$20,00"
        )
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is True
        assert len(nota["parceiros"]) == 1
        p = nota["parceiros"]["12345678000199"]
        assert p["cota_parceiro"] == 60.0  # 40 + 20
        assert p["cota_salao"] == 90.0  # 60 + 30

    def test_campos_xml_extraidos(self):
        """Verifica extração correta dos campos XML."""
        xml = _build_xml(
            nnfse="999",
            dcompet="2026-03-10",
            dhemi="2026-03-10T14:30:00",
            dhproc="2026-03-11T09:00:00",
            vserv="350.50",
            xdesc="Serviço sem rateio",
        )
        doc = _build_doc(xml, chave="ABC123")
        nota = en.extrair_dados_nota(doc)

        assert nota["nfse"] == "999"
        assert nota["data_servico"] == "2026-03-10"
        assert nota["data_emissao"] == "2026-03-11"
        assert nota["valor_total"] == 350.50
        assert nota["chave_acesso"] == "ABC123"

    def test_formato2_multiplos_blocos(self):
        """Formato 2 com múltiplos blocos de rateio (mesmo parceiro acumula)."""
        desc = (
            "Rateio referente a Salao/Profissional parceiro: "
            "CNPJ: 09223558000100 - DEPILAGOS - R$ 100,00 "
            "CNPJ: 55555555000100 - PARCEIRO - R$ 50,00 "
            "Rateio referente a Salao/Profissional parceiro: "
            "CNPJ: 09223558000100 - DEPILAGOS - R$ 80,00 "
            "CNPJ: 55555555000100 - PARCEIRO - R$ 30,00"
        )
        xml = _build_xml(xdesc=desc)
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)

        assert nota["tem_rateio"] is True
        p = nota["parceiros"]["55555555000100"]
        assert p["cota_parceiro"] == 80.0  # 50 + 30
        assert p["cota_salao"] == 180.0  # 100 + 80


# === Testes extrair_notas_pdf ===

class TestExtrairNotasPdf:
    """Testes para extrair_notas_pdf com mock de pdftotext."""

    def _mock_pdftotext(self, text):
        """Retorna side_effect que escreve `text` no arquivo tmp."""
        def side_effect(cmd, **kwargs):
            tmp_path = cmd[2]  # pdftotext input output
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(text)
            return MagicMock(returncode=0)
        return side_effect

    @patch("extrair_notas.subprocess.run")
    def test_nota_com_rateio(self, mock_run):
        pdf_text = (
            "Nota Fiscal de Serviço Eletrônica\n"
            "Número da NFS-e: 42\n"
            "15/02/2026\n\n"
            "ABCDEFGHIJ\n"
            "Rateio\n"
            "CNPJ: 09223558000100 - DEPILAGOS - R$ 100,00 "
            "CNPJ: 12345678000199 - PARCEIRO - R$ 50,00\n"
        )
        mock_run.side_effect = self._mock_pdftotext(pdf_text)
        notas = en.extrair_notas_pdf(["/fake/notas.pdf"])

        assert len(notas) == 1
        assert notas[0]["nfse"] == "42"
        assert notas[0]["tem_rateio"] is True
        assert "12345678000199" in notas[0]["parceiros"]
        assert notas[0]["parceiros"]["12345678000199"]["cota_parceiro"] == 50.0
        assert notas[0]["fonte"] == "pdf"

    @patch("extrair_notas.subprocess.run")
    def test_nota_sem_rateio_ignorada(self, mock_run):
        pdf_text = (
            "Nota Fiscal de Serviço Eletrônica\n"
            "Número da NFS-e: 99\n"
            "Serviço de depilação sem rateio\n"
        )
        mock_run.side_effect = self._mock_pdftotext(pdf_text)
        notas = en.extrair_notas_pdf(["/fake/notas.pdf"])
        assert len(notas) == 0

    @patch("extrair_notas.subprocess.run")
    def test_multiplos_parceiros_pdf(self, mock_run):
        pdf_text = (
            "Nota Fiscal de Serviço Eletrônica\n"
            "Número da NFS-e: 77\n"
            "10/03/2026\n\n"
            "ABCDEFGHIJ\n"
            "Rateio\n"
            "CNPJ: 09223558000100 - DEPILAGOS - R$ 200,00 "
            "CNPJ: 11111111000100 - PARCEIRO A - R$ 60,00 "
            "CNPJ: 22222222000100 - PARCEIRO B - R$ 40,00\n"
        )
        mock_run.side_effect = self._mock_pdftotext(pdf_text)
        notas = en.extrair_notas_pdf(["/fake/notas.pdf"])

        assert len(notas) == 1
        assert len(notas[0]["parceiros"]) == 2
        assert "11111111000100" in notas[0]["parceiros"]
        assert "22222222000100" in notas[0]["parceiros"]


# === Testes main() (integração) ===

class TestMain:
    """Testes de integração para main() com mocks de API e filesystem."""

    def _make_api_response(self, docs, status="PROCESSAMENTO_COMPLETO"):
        """Cria resposta da API simulada."""
        return {"StatusProcessamento": status, "LoteDFe": docs}

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_gera_csv_com_formato_correto(self, mock_lote, mock_cert, mock_glob):
        """Verifica formato do CSV: delimitador ;, vírgula decimal, colunas."""
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$120,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$80,00"
        )
        xml = _build_xml(nnfse="10", dcompet="2026-02-15", dhproc="2026-02-16T08:00:00", xdesc=desc)
        doc = _build_doc(xml)

        mock_lote.side_effect = [
            self._make_api_response([doc]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            output_path = f.name

        try:
            with patch("sys.argv", ["extrair_notas.py", "--output", output_path, "--senha", "test"]):
                en.main()

            with open(output_path, encoding="utf-8") as f:
                lines = f.readlines()

            # Header
            assert lines[0].strip() == (
                "data servico;data emissao;NUMERO DA NOTA;CNPJ PROFISSIONAL PARCEIRO;"
                "COTA PARTE SALÃO PARCEIRO;COTA PARTE PROFISSIONAL-PARCEIRO"
            )
            # Data line
            cols = lines[1].strip().split(";")
            assert cols[0] == "15/02/2026"  # data servico DD/MM/YYYY
            assert cols[1] == "16/02/2026"  # data emissao DD/MM/YYYY
            assert cols[2] == "10"  # numero nota
            assert cols[3] == "12.345.678/0001-99"  # CNPJ formatado
            assert cols[4] == "120,00"  # cota salão com vírgula
            assert cols[5] == "80,00"  # cota parceiro com vírgula
        finally:
            os.unlink(output_path)

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_filtro_por_periodo(self, mock_lote, mock_cert, mock_glob):
        """Notas fora do período são excluídas."""
        desc_rateio = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$60,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$40,00"
        )
        doc_fev = _build_doc(_build_xml(nnfse="1", dcompet="2026-02-10", xdesc=desc_rateio))
        doc_mar = _build_doc(_build_xml(nnfse="2", dcompet="2026-03-05", xdesc=desc_rateio), nsu=2)

        mock_lote.side_effect = [
            self._make_api_response([doc_fev, doc_mar]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            output_path = f.name

        try:
            with patch("sys.argv", ["extrair_notas.py", "--output", output_path,
                                     "--periodo", "2026-02", "--senha", "test"]):
                en.main()

            with open(output_path, encoding="utf-8") as f:
                lines = f.readlines()

            assert len(lines) == 2  # header + 1 nota de fevereiro
            assert "10/02/2026" in lines[1]
        finally:
            os.unlink(output_path)

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_notas_ordenadas_por_numero(self, mock_lote, mock_cert, mock_glob):
        """CSV deve ter notas ordenadas por número."""
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$50,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$50,00"
        )
        doc_300 = _build_doc(_build_xml(nnfse="300", xdesc=desc), nsu=1)
        doc_100 = _build_doc(_build_xml(nnfse="100", xdesc=desc), nsu=2)
        doc_200 = _build_doc(_build_xml(nnfse="200", xdesc=desc), nsu=3)

        mock_lote.side_effect = [
            self._make_api_response([doc_300, doc_100, doc_200]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            output_path = f.name

        try:
            with patch("sys.argv", ["extrair_notas.py", "--output", output_path, "--senha", "test"]):
                en.main()

            with open(output_path, encoding="utf-8") as f:
                lines = f.readlines()

            numeros = [line.split(";")[2] for line in lines[1:]]
            assert numeros == ["100", "200", "300"]
        finally:
            os.unlink(output_path)

    @patch("extrair_notas.extrair_notas_pdf")
    @patch("extrair_notas.glob.glob", return_value=["/fake/Notas.pdf"])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_complemento_pdf_deduplicacao(self, mock_lote, mock_cert, mock_glob, mock_pdf):
        """Notas do PDF não presentes na API são adicionadas; duplicatas ignoradas."""
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$50,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$50,00"
        )
        doc_api = _build_doc(_build_xml(nnfse="10", xdesc=desc))

        mock_lote.side_effect = [
            self._make_api_response([doc_api]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        # PDF retorna nota 10 (duplicata) e nota 20 (nova)
        mock_pdf.return_value = [
            {
                "nfse": "10", "chave_acesso": "", "data_servico": "2026-02-10",
                "data_emissao": "27/02/2026", "valor_total": 0.0, "descricao": "",
                "parceiros": {"12345678000199": {"cota_parceiro": 50.0, "cota_salao": 50.0}},
                "tem_rateio": True, "nsu": 0, "fonte": "pdf",
            },
            {
                "nfse": "20", "chave_acesso": "", "data_servico": "2026-02-12",
                "data_emissao": "27/02/2026", "valor_total": 0.0, "descricao": "",
                "parceiros": {"98765432000111": {"cota_parceiro": 30.0, "cota_salao": 70.0}},
                "tem_rateio": True, "nsu": 0, "fonte": "pdf",
            },
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            output_path = f.name

        try:
            with patch("sys.argv", ["extrair_notas.py", "--output", output_path, "--senha", "test"]):
                en.main()

            with open(output_path, encoding="utf-8") as f:
                lines = f.readlines()

            # Header + nota 10 (API) + nota 20 (PDF) = 3 linhas
            assert len(lines) == 3
            numeros = [line.split(";")[2] for line in lines[1:]]
            assert "10" in numeros
            assert "20" in numeros
        finally:
            os.unlink(output_path)

    @patch("extrair_notas.extrair_notas_pdf")
    @patch("extrair_notas.glob.glob", return_value=["/fake/Notas.pdf"])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_pdf_nota_formato_data_emissao_preservado(self, mock_lote, mock_cert, mock_glob, mock_pdf):
        """Notas vindas do PDF mantêm data_emissao no formato original (DD/MM/YYYY)."""
        mock_lote.side_effect = [
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        mock_pdf.return_value = [
            {
                "nfse": "50", "chave_acesso": "", "data_servico": "2026-02-20",
                "data_emissao": "27/02/2026", "valor_total": 0.0, "descricao": "",
                "parceiros": {"12345678000199": {"cota_parceiro": 40.0, "cota_salao": 60.0}},
                "tem_rateio": True, "nsu": 0, "fonte": "pdf",
            },
        ]

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            output_path = f.name

        try:
            with patch("sys.argv", ["extrair_notas.py", "--output", output_path, "--senha", "test"]):
                en.main()

            with open(output_path, encoding="utf-8") as f:
                lines = f.readlines()

            cols = lines[1].strip().split(";")
            # PDF data_emissao já vem em DD/MM/YYYY, não deve converter de novo
            assert cols[1] == "27/02/2026"
        finally:
            os.unlink(output_path)
