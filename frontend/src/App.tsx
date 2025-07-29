import { useState, type ChangeEvent } from "react";
import axios from "axios";
import { DashboardSummary } from "./components/DashboardSummary";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";

type Vulnerability = {
  id: string;
  summary: string;
  details?: string;
  cvss_v4_vector?: string;
  score?: number;
  level?: string;
  references: { url: string }[];
};

type ScanResult = {
  package: {
    name: string;
    version: string;
  };
  vulnerabilities: Vulnerability[];
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<ScanResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<ScanResult[]>(
        "http://127.0.0.1:8000/scan-file",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResults(response.data);
    } catch (error) {
      console.error("Erro ao enviar arquivo:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="font-jet min-h-screen bg-gray-900 text-white pt-24 px-6 py-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <Navbar />
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg space-y-4">
          <h3 className="text-2xl font-bold text-purple-400">Ecosistemas suportados:</h3>
          <p>• Python | requirements.txt</p>
          <p>• JavaScript | package.json</p>
          <p>• PHP | composer.json</p>
          <p>• Ruby | Gemfile</p>
          <p>• Kotlin | build.gradle</p>
          <p>• Java | pom.xml</p>
        </div>

        {/* Upload e Botão */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg space-y-4">
          <label className="block">
            <span className="text-sm text-gray-300">Envie as suas dependências:</span>
            <input
              type="file"
              accept=".txt, .json, .xml, .gradle, Gemfile"
              onChange={handleFileChange}
              className="mt-1 block w-full text-sm text-white bg-gray-700 border border-gray-600 rounded p-2"
            />
          </label>
          <button
            onClick={handleUpload}
            className="bg-purple-600 hover:bg-purple-700 transition px-6 py-2 rounded font-semibold w-full sm:w-auto"
            disabled={loading}
          >
            {loading ? "Analisando..." : "Analisar dependências"}
          </button>
        </div>
        {/* Resultados */}
        {results.length >= 0 && (
          <div className="space-y-6 h-svh">
            <DashboardSummary results={results} />

            {results.map((res, i) => (
              <div
                key={i}
                className="border border-purple-600 rounded bg-gray-800 shadow-md mb-4"
              >
                <button
                  onClick={() => setOpenIndex(openIndex === i ? null : i)} // 👈 Alterna só o índice atual
                  className="w-full text-left px-4 py-3 bg-gray-900 hover:bg-gray-700 transition font-semibold text-purple-300 flex justify-between items-center"
                >
                  📦 {res.package.name}@{res.package.version}
                  <span className="text-sm text-gray-400">
                    {openIndex === i ? "▲" : "▼"}
                  </span>
                </button>

                {openIndex === i && (
                  <div className="p-4 space-y-4">
                    {res.vulnerabilities.length > 0 ? (
                      <ul className="space-y-2">
                        {res.vulnerabilities.map((vuln, idx) => (
                          <li
                            key={idx}
                            className="bg-gray-700 p-4 rounded border-l-4 border-red-600 space-y-2"
                          >
                            <div>
                              <strong>{vuln.id}</strong>: {vuln.summary}
                            </div>

                            {vuln.level && (
                              <div className="text-sm">
                                🧪 <span className="text-white font-semibold">Score:</span>{" "}
                                {vuln.score ?? "N/A"} ({vuln.level})
                              </div>
                            )}

                            {vuln.cvss_v4_vector && (
                              <div className="text-xs text-gray-400 italic">
                                🧬 {vuln.cvss_v4_vector}
                              </div>
                            )}

                            {vuln.references.length > 0 && (
                              <div>
                                🔗{" "}
                                <a
                                  href={vuln.references[0].url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="underline text-blue-400"
                                >
                                  Ver mais
                                </a>
                              </div>
                            )}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-green-400">✅ Sem vulnerabilidades conhecidas</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
        <Footer />
      </div>
    </div>
  );
}

export default App;