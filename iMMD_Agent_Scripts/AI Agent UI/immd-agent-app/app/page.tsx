import ChatBox from './components/ChatBox';

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold text-center mb-8">
        iMMD AI Agent Chat
      </h1>
      <ChatBox />
    </main>
  );
}
