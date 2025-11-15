export default function TopBar() {
  return (
    <div className="fixed top-8 right-8 z-50">
      <div className="bg-white rounded-full shadow-lg px-6 py-3 flex items-center gap-4">
        <button className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-full font-medium transition-colors flex items-center gap-2">
          <span>▶</span>
          Run
        </button>
      </div>
    </div>
  );
}
