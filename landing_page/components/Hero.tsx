"use client";
import React, { useState } from 'react';
import MeshBackground from './MeshBackground';

const Hero = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Simulating form submission to Formspree or similar
    console.log(`Signing up ${email}...`);
    setSubmitted(true);
  };

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center text-center px-6 overflow-hidden">
      <MeshBackground />

      <div className="relative z-10 max-w-4xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-brand font-bold text-text-primary leading-tight mb-6">
          Your files. Your network. <br />
          <span className="text-accent">No cloud required.</span>
        </h1>
        <p className="text-lg md:text-xl text-text-secondary mb-10 max-w-2xl mx-auto font-body">
          ShulkerBox connects your devices directly — no middleman, no subscription, no data leaving your hands.
        </p>

        {!submitted ? (
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 justify-center max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="px-6 py-3 rounded-full bg-background-secondary border border-white/10 text-text-primary outline-none focus:border-accent transition-colors flex-grow"
            />
            <button
              type="submit"
              className="px-6 py-3 rounded-full bg-accent text-black font-bold transition-transform hover:scale-105 active:scale-95"
            >
              Join Pioneer Access
            </button>
          </form>
        ) : (
          <div className="text-accent font-bold text-xl animate-fade-in">
            You're in. We'll reach out when Pioneer Access opens.
          </div>
        )}

        <p className="mt-4 text-sm text-text-secondary font-body">
          Be among the first 100 Pioneers
        </p>
      </div>
    </section>
  );
};

export default Hero;
