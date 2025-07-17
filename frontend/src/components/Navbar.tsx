
export const Navbar = () => {
  return (
    <header className="bg-gray-900 fixed top-0 left-0 w-full z-50 shadow-md border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="text-purple-500 text-2xl font-bold">CodeWard</div>
        <nav className="hidden md:flex space-x-6 text-white font-medium">
          <a href="#dashboard" className="hover:text-purple-400">Dashboard</a>
          <a href="#detalhes" className="hover:text-purple-400">Detalhes</a>
          <a href="#planos" className="hover:text-purple-400">Planos</a>
          <a href="#contato" className="hover:text-purple-400">Contato</a>
        </nav>
        <a
          href="/"
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded font-semibold text-sm"
        >
          Comece agora
        </a>
      </div>
    </header>

  );
};
