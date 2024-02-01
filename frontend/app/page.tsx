import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-evenly	 gap-10 p-10 background-gradient">
      <Header />
      <ChatSection />
    </main>
  );
}
