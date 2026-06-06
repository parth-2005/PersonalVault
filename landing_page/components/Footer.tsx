import React from 'react';

const Footer = () => {
  return (
    <footer className="py-12 px-6 border-t border-white/10 bg-background">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex flex-col items-center md:items-start gap-2">
          <div className="text-xl font-brand font-bold text-text-primary">
            ShulkerBox
          </div>
          <p className="text-sm text-text-secondary font-body italic">
            "Your files. Your network. No cloud required."
          </p>
        </div>

        <div className="flex flex-col items-center md:items-end gap-4">
          <div className="flex gap-6 text-sm text-text-secondary font-body">
            <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-accent transition-colors">GitHub</a>
            <a href="#privacy" className="hover:text-accent transition-colors">Privacy</a>
          </div>
          <p className="text-xs text-text-secondary font-body opacity-50">
            © 2026 ShulkerBox. Open source. Built for humans.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
