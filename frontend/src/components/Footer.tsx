export const Footer = () => {
  return (
    <footer className="bg-gray-900 bottom-0 left-0 w-full z-50 shadow-md border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="text-purple-500 font-bold">© CodeWard - Todos os direitos reservados.</div>
        <nav className="hidden md:flex space-x-6 text-white font-medium">
          <a href="#dashboard" className="hover:text-purple-400">Instagram</a>
          <a href="#dashboard" className="hover:text-purple-400">Linkedin</a>
          <a href="#dashboard" className="hover:text-purple-400">Contato</a>
        </nav>
        <a href="/" className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded font-semibold text-sm">Be Safe, Be CodeWard</a>
      </div>
    </footer>
  )
}