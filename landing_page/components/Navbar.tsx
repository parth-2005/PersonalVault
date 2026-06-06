import React from 'react';
import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 flex items-center justify-between px-6 py-4 backdrop-blur-sm bg-background/80 border-b border-white/10">
      <div className="flex items-center gap-2">
        <Link href="/" className="text-xl font-brand font-bold tracking-tighter text-text-primary">
          ShulkerBox
        </Link>
      </div>
      <div className="flex items-center gap-4">
        <Link
          href="#pioneer-access"
          className="px-4 py-2 rounded-full bg-accent text-black font-body font-semibold text-sm transition-transform hover:scale-105 active:scale-95"
        >
          Pioneer Access
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
