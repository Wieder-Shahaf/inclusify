import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Navbar />
      <main className="container-px mx-auto max-w-7xl">
        {children}
      </main>
      <Footer />
    </>
  );
}
