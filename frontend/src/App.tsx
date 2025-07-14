import { useState, type ChangeEvent } from "react";
import axios from "axios";

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
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">🛡️ CodeWard</h1>

      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-purple-600 px-4 py-2 rounded hover:bg-purple-700 transition"
        disabled={loading}
      >
        {loading ? "Analisando..." : "Analisar dependências"}
      </button>

      {results.length > 0 && (
        <div className="mt-8 space-y-6">
          {results.map((res, i) => (
            <div
              key={i}
              className="border border-purple-500 rounded p-4 bg-gray-800"
            >
              <h2 className="text-xl font-semibold">
                📦 {res.package.name}@{res.package.version}
              </h2>
              {res.vulnerabilities.length > 0 ? (
                <ul className="mt-2 space-y-2">
                  {res.vulnerabilities.map((vuln, idx) => (
                    <li key={idx} className="bg-red-900 p-3 rounded space-y-1">
                      <strong>{vuln.id}</strong>: {vuln.summary}
                      {vuln.level && (
                        <div className="text-sm mt-1">
                          🧪 <span className="text-white font-semibold">Score:</span> {vuln.score ?? "N/A"} ({vuln.level})
                        </div>
                      )}
                      {vuln.cvss_v4_vector && (
                        <div className="text-xs text-gray-400 italic">
                          🧬 {vuln.cvss_v4_vector}
                        </div>
                      )}
                      {vuln.references.length > 0 && (
                        <div className="mt-1">
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
                <p className="text-green-400 mt-2">
                  ✅ Sem vulnerabilidades conhecidas
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
