"""Testes unitários para funcionalidade de resumo em extrair_notas.py."""

import base64
import gzip
import os
import tempfile
from unittest.mock import patch

import pytest

import extrair_notas as en

CSV_HEADER = ("data servico;data emissao;NUMERO DA NOTA;CNPJ PROFISSIONAL PARCEIRO;"
              "COTA PARTE SALÃO PARCEIRO;COTA PARTE PROFISSIONAL-PARCEIRO\n")

# === Helpers ===

NS_DECL = 'xmlns="http://www.sped.fazenda.gov.br/nfse"'


def _build_xml(nnfse="100", dcompet="2026-02-15", dhemi="2026-02-15T10:00:00",
               dhproc="2026-02-16T08:00:00", vserv="200.00", xdesc="",
               cstat=None):
    """Constrói um XML NFS-e mínimo, opcionalmente com cStat."""
    cstat_xml = f"<cStat>{cstat}</cStat>" if cstat else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<NFSe {NS_DECL}>
  <infNFSe>
    <nNFSe>{nnfse}</nNFSe>
    <dCompet>{dcompet}</dCompet>
    <dhEmi>{dhemi}</dhEmi>
    <dhProc>{dhproc}</dhProc>
    {cstat_xml}
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


def _nota(nfse="100", data="2026-02-15", valor=200.0, tem_rateio=False, cstat="100"):
    """Cria dict de nota para testar gerar_resumo()."""
    return {
        "nfse": nfse,
        "data_servico": data,
        "valor_total": valor,
        "tem_rateio": tem_rateio,
        "cstat": cstat,
    }


# === Testes extrair_dados_nota com cStat ===

class TestExtrairDadosNotaCstat:
    """Testes para extração do campo cStat."""

    def test_cstat_presente(self):
        xml = _build_xml(cstat="110", xdesc="Servico teste")
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)
        assert nota["cstat"] == "110"

    def test_cstat_ausente_default_100(self):
        xml = _build_xml(xdesc="Servico teste")
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)
        assert nota["cstat"] == "100"

    def test_cstat_autorizada(self):
        xml = _build_xml(cstat="100", xdesc="Servico teste")
        doc = _build_doc(xml)
        nota = en.extrair_dados_nota(doc)
        assert nota["cstat"] == "100"


# === Testes gerar_resumo ===

class TestGerarResumo:
    """Testes para gerar_resumo()."""

    def test_resumo_basico(self):
        notas = [
            _nota(nfse="1", valor=100.0),
            _nota(nfse="2", valor=200.0, tem_rateio=True),
        ]
        resumo = en.gerar_resumo(notas, "2026-02")

        assert "RESUMO MENSAL DE NOTAS FISCAIS - 2026-02" in resumo
        assert "Autorizadas:  2" in resumo
        assert "TOTAL:        2" in resumo
        assert "R$ 300,00" in resumo

    def test_canceladas_nao_entram_no_total(self):
        notas = [
            _nota(nfse="1", valor=100.0, cstat="100"),
            _nota(nfse="2", valor=500.0, cstat="110"),
        ]
        resumo = en.gerar_resumo(notas, "2026-02")

        assert "Autorizadas:  1" in resumo
        assert "Canceladas:   1" in resumo
        assert "TOTAL:        2" in resumo
        assert "Total de notas:    1" in resumo
        assert "R$ 100,00" in resumo
        # Valor da cancelada NÃO deve estar no total
        assert "R$ 500,00" not in resumo

    def test_breakdown_rateio(self):
        notas = [
            _nota(nfse="1", valor=100.0, tem_rateio=True),
            _nota(nfse="2", valor=200.0, tem_rateio=True),
            _nota(nfse="3", valor=50.0, tem_rateio=False),
        ]
        resumo = en.gerar_resumo(notas, "2026-02")

        assert "Com rateio:    2 notas  |  R$ 300,00" in resumo
        assert "Sem rateio:    1 notas  |  R$ 50,00" in resumo

    def test_valor_por_dia(self):
        notas = [
            _nota(nfse="1", data="2026-02-10", valor=100.0),
            _nota(nfse="2", data="2026-02-10", valor=50.0),
            _nota(nfse="3", data="2026-02-15", valor=200.0),
        ]
        resumo = en.gerar_resumo(notas, "2026-02")

        assert "10/02/2026" in resumo
        assert "15/02/2026" in resumo

    def test_sem_notas(self):
        resumo = en.gerar_resumo([], "2026-03")

        assert "RESUMO MENSAL DE NOTAS FISCAIS - 2026-03" in resumo
        assert "Autorizadas:  0" in resumo
        assert "R$ 0,00" in resumo

    def test_canceladas_ocultas_se_nao_existem(self):
        notas = [_nota(nfse="1", valor=100.0)]
        resumo = en.gerar_resumo(notas, "2026-02")
        assert "Canceladas" not in resumo

    def test_outros_status(self):
        notas = [
            _nota(nfse="1", valor=100.0, cstat="100"),
            _nota(nfse="2", valor=50.0, cstat="999"),
        ]
        resumo = en.gerar_resumo(notas, "2026-02")
        assert "Outros:       1" in resumo


# === Testes integração main() com resumo ===

class TestMainResumo:
    """Testes de integração para geração do resumo no main()."""

    def _make_api_response(self, docs, status="PROCESSAMENTO_COMPLETO"):
        return {"StatusProcessamento": status, "LoteDFe": docs}

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_gera_resumo_com_periodo(self, mock_lote, mock_cert, mock_glob):
        """Quando --periodo é passado, gera arquivo de resumo .txt."""
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$120,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$80,00"
        )
        xml = _build_xml(nnfse="10", dcompet="2026-02-15", vserv="200.00", xdesc=desc)
        doc = _build_doc(xml)

        mock_lote.side_effect = [
            self._make_api_response([doc]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "notas.csv")
            resumo_path = os.path.join(tmpdir, "resumo_fev2026.txt")

            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                resumo_expected = os.path.join(tmpdir, "output", "resumo_fev2026.txt")
                with patch("sys.argv", ["extrair_notas.py", "--output", csv_path,
                                         "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                assert os.path.exists(resumo_expected)
                with open(resumo_expected, encoding="utf-8") as f:
                    content = f.read()
                assert "RESUMO MENSAL" in content
                assert "R$ 200,00" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_sem_periodo_nao_gera_resumo(self, mock_lote, mock_cert, mock_glob):
        """Sem --periodo, não gera arquivo de resumo."""
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$100,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$50,00"
        )
        xml = _build_xml(nnfse="5", xdesc=desc)
        doc = _build_doc(xml)

        mock_lote.side_effect = [
            self._make_api_response([doc]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "notas.csv")
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                with patch("sys.argv", ["extrair_notas.py", "--output", csv_path, "--senha", "test"]):
                    en.main()

            # Nenhum .txt deve existir
            txt_files = [f for f in os.listdir(tmpdir) if f.endswith(".txt")]
            assert len(txt_files) == 0


# === Testes contar_registros_csv ===

class TestContarRegistrosCsv:
    def test_conta_linhas_de_dados(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(CSV_HEADER + "l1\nl2\nl3\n")
        assert en.contar_registros_csv(str(csv)) == 3

    def test_ignora_linhas_vazias(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(CSV_HEADER + "l1\n\nl2\n\n")
        assert en.contar_registros_csv(str(csv)) == 2

    def test_csv_so_cabecalho(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text(CSV_HEADER)
        assert en.contar_registros_csv(str(csv)) == 0


# === Testes ler_historico ===

class TestLerHistorico:
    def test_arquivo_nao_existe(self):
        assert en.ler_historico("/tmp/nao_existe_xyz.txt") == []

    def test_resumo_sem_historico(self, tmp_path):
        resumo = tmp_path / "resumo.txt"
        resumo.write_text("RESUMO MENSAL\nalguma coisa\n")
        assert en.ler_historico(str(resumo)) == []

    def test_le_historico_existente(self, tmp_path):
        resumo = tmp_path / "resumo.txt"
        resumo.write_text(
            "RESUMO MENSAL\n\n"
            "HISTÓRICO DE ATUALIZAÇÕES\n"
            "--------------------------------------------------\n"
            "  28/02/2026  Primeira extração: 536 registros\n"
            "  28/02/2026  Atualização: 536 → 553 registros (+17 notas)\n"
        )
        entries = en.ler_historico(str(resumo))
        assert len(entries) == 2
        assert "Primeira extração: 536 registros" in entries[0]
        assert "Atualização: 536 → 553" in entries[1]


# === Testes gerar_resumo com histórico ===

class TestGerarResumoHistorico:
    def test_sem_historico_nao_inclui_secao(self):
        resumo = en.gerar_resumo([], "2026-02")
        assert "HISTÓRICO" not in resumo

    def test_com_historico_inclui_secao(self):
        hist = ["28/02/2026  Primeira extração: 10 registros"]
        resumo = en.gerar_resumo([], "2026-02", historico=hist)
        assert "HISTÓRICO DE ATUALIZAÇÕES" in resumo
        assert "Primeira extração: 10 registros" in resumo

    def test_historico_vazio_nao_inclui_secao(self):
        resumo = en.gerar_resumo([], "2026-02", historico=[])
        assert "HISTÓRICO" not in resumo


# === Testes auto-output e comparação no main() ===

class TestMainComparacao:
    """Testes para lógica de comparação com CSV existente."""

    def _make_api_response(self, docs, status="PROCESSAMENTO_COMPLETO"):
        return {"StatusProcessamento": status, "LoteDFe": docs}

    def _make_doc(self, nnfse="10", dcompet="2026-02-15"):
        desc = (
            "SALAO-PARCEIRO: 09223558000100 COTA-PARTE R$120,00 "
            "PROFISSIONAL-PARCEIRO: 12345678000199 COTA-PARTE R$80,00"
        )
        xml = _build_xml(nnfse=nnfse, dcompet=dcompet, vserv="200.00", xdesc=desc)
        return _build_doc(xml, nsu=int(nnfse))

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_csv_nao_existe_primeira_extracao(self, mock_lote, mock_cert, mock_glob):
        """CSV não existe → cria tudo, registra 'Primeira extração'."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")
                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                assert os.path.exists(csv_path)
                assert os.path.exists(resumo_path)
                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                assert "Primeira extração: 1 registros" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_csv_existente_sem_diferenca(self, mock_lote, mock_cert, mock_glob):
        """CSV existe com mesmo conteúdo → não sobrescreve, registra verificação."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")

                # Pré-criar CSV com 1 registro
                with open(csv_path, "w", encoding="utf-8") as f:
                    f.write(CSV_HEADER)
                    f.write("15/02/2026;16/02/2026;10;12.345.678/0001-99;120,00;80,00\n")

                mtime_before = os.path.getmtime(csv_path)

                # Pequena pausa para garantir diferença de mtime se houver escrita
                import time
                time.sleep(0.05)

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                mtime_after = os.path.getmtime(csv_path)
                assert mtime_before == mtime_after, "CSV não deveria ter sido sobrescrito"

                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")
                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                assert "Verificação: sem notas novas (1 registros)" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_csv_existente_com_notas_novas(self, mock_lote, mock_cert, mock_glob):
        """CSV existe mas API retorna mais notas → sobrescreve e registra atualização."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc("10"), self._make_doc("20", "2026-02-16")]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")

                # Pré-criar CSV com 1 registro
                with open(csv_path, "w", encoding="utf-8") as f:
                    f.write(CSV_HEADER)
                    f.write("15/02/2026;16/02/2026;10;12.345.678/0001-99;120,00;80,00\n")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                # CSV deve ter 2 registros agora
                assert en.contar_registros_csv(csv_path) == 2

                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")
                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                assert "Atualização: 1 → 2 registros (+1 notas)" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_historico_preservado(self, mock_lote, mock_cert, mock_glob):
        """Histórico anterior do resumo é preservado ao atualizar."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")
                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")

                # Pré-criar resumo com histórico
                with open(resumo_path, "w", encoding="utf-8") as f:
                    f.write("RESUMO MENSAL DE NOTAS FISCAIS - 2026-02\n\n"
                            "HISTÓRICO DE ATUALIZAÇÕES\n"
                            "--------------------------------------------------\n"
                            "  25/02/2026  Primeira extração: 500 registros\n\n")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02",
                                         "--output", csv_path, "--senha", "test"]):
                    en.main()

                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                # Histórico anterior preservado
                assert "25/02/2026  Primeira extração: 500 registros" in content
                # Nova entrada adicionada
                assert "Primeira extração: 1 registros" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_auto_output_com_periodo(self, mock_lote, mock_cert, mock_glob):
        """--periodo 2026-02 sem --output → output/fev2026.csv."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                expected_csv = os.path.join(tmpdir, "output", "fev2026.csv")
                assert os.path.exists(expected_csv)
                assert en.contar_registros_csv(expected_csv) == 1

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_csv_existente_com_menos_registros(self, mock_lote, mock_cert, mock_glob):
        """CSV existe com mais registros que a API → sobrescreve e registra com diff negativo."""
        # API retorna 1 nota, mas CSV tem 2
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc("10")]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")

                # Pré-criar CSV com 2 registros
                with open(csv_path, "w", encoding="utf-8") as f:
                    f.write(CSV_HEADER)
                    f.write("15/02/2026;16/02/2026;10;12.345.678/0001-99;120,00;80,00\n")
                    f.write("16/02/2026;17/02/2026;20;12.345.678/0001-99;100,00;60,00\n")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                # CSV deve ter sido sobrescrito com 1 registro
                assert en.contar_registros_csv(csv_path) == 1

                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")
                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                assert "Atualização: 2 → 1 registros (-1 notas)" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_csv_existente_sem_periodo_nao_compara(self, mock_lote, mock_cert, mock_glob):
        """Sem --periodo, CSV existente é sobrescrito sem comparação (sem histórico)."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "notas.csv")

            # Pré-criar CSV com conteúdo diferente
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write(CSV_HEADER)
                f.write("old;data;here;content;0;0\n")
                f.write("old;data;here2;content;0;0\n")

            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"), exist_ok=True)
                with patch("sys.argv", ["extrair_notas.py", "--output", csv_path, "--senha", "test"]):
                    en.main()

            # CSV sobrescrito com 1 registro (sem comparação)
            assert en.contar_registros_csv(csv_path) == 1

            # Sem resumo gerado
            txt_files = [f for f in os.listdir(tmpdir) if f.endswith(".txt")]
            assert len(txt_files) == 0

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_api_retorna_zero_notas_csv_existe(self, mock_lote, mock_cert, mock_glob):
        """API retorna 0 notas com rateio mas CSV existe → sobrescreve com 0 registros."""
        # Nota sem rateio
        xml = _build_xml(nnfse="10", dcompet="2026-02-15", vserv="200.00",
                         xdesc="Serviço sem rateio nenhum")
        doc = _build_doc(xml, nsu=10)

        mock_lote.side_effect = [
            self._make_api_response([doc]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                csv_path = os.path.join(tmpdir, "output", "fev2026.csv")

                # Pré-criar CSV com 3 registros
                with open(csv_path, "w", encoding="utf-8") as f:
                    f.write(CSV_HEADER)
                    f.write("l1\nl2\nl3\n")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02", "--senha", "test"]):
                    en.main()

                assert en.contar_registros_csv(csv_path) == 0

                resumo_path = os.path.join(tmpdir, "output", "resumo_fev2026.txt")
                with open(resumo_path, encoding="utf-8") as f:
                    content = f.read()
                assert "Atualização: 3 → 0 registros (-3 notas)" in content

    @patch("extrair_notas.glob.glob", return_value=[])
    @patch("extrair_notas.extrair_cert_key", return_value=("/tmp/cert.pem", "/tmp/key.pem"))
    @patch("extrair_notas.consultar_lote")
    def test_output_explicito_com_periodo(self, mock_lote, mock_cert, mock_glob):
        """--output explícito com --periodo usa o output passado, não auto-detecta."""
        mock_lote.side_effect = [
            self._make_api_response([self._make_doc()]),
            self._make_api_response([], "NENHUM_DOCUMENTO_LOCALIZADO"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("extrair_notas.PROJETO_DIR", tmpdir):
                os.makedirs(os.path.join(tmpdir, "output"))
                custom_path = os.path.join(tmpdir, "custom.csv")

                with patch("sys.argv", ["extrair_notas.py", "--periodo", "2026-02",
                                         "--output", custom_path, "--senha", "test"]):
                    en.main()

                assert os.path.exists(custom_path)
                # Auto-output NÃO deve ter sido criado
                auto_path = os.path.join(tmpdir, "output", "fev2026.csv")
                assert not os.path.exists(auto_path)
