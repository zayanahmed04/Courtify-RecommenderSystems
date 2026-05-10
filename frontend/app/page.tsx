export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-emerald-700 mb-2">CourtFind AI</h1>
      <p className="text-gray-600 mb-8 text-center max-w-md">
        AI-powered sports court discovery and player matchmaking for Karachi.
      </p>
      <div className="flex gap-4">
        <a
          href="/courts"
          className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition"
        >
          Find Courts
        </a>
        <a
          href="/matchmaking"
          className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition"
        >
          Find Players
        </a>
      </div>
    </main>
  );
}
