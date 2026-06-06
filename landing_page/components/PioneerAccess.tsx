"use client";
import React, { useState } from 'react';

const PioneerAccess = () => {
  const [email, setEmail] = useState('');
  const [useCase, setUseCase] = useState('Personal file sync');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log(`Joining pioneers: ${email}, ${useCase}`);
    setSubmitted(true);
  };

  return (
    <section id="pioneer-access" className="py-24 px-6 border-t border-accent/20">
      <div className="max-w-4xl mx-auto text-center bg-background-secondary p-12 rounded-3xl border-2 border-accent/30 shadow-[0_0_50px_rgba(245,166,35,0.1)]">
        <h2 className="text-3xl md:text-5xl font-brand font-bold text-text-primary mb-4">
          Become a Pioneer
        </h2>
        <p className="text-text-secondary font-body mb-10 max-w-2xl mx-auto">
          We're opening early access to a small group of testers. Help shape ShulkerBox before it launches.
        </p>

        {!submitted ? (
          <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-md mx-auto">
            <input
              type="email"
              placeholder="Email address"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="px-6 py-3 rounded-lg bg-background border border-white/10 text-text-primary outline-none focus:border-accent transition-colors"
            />
            <select
              value={useCase}
              onChange={(e) => setUseCase(e.target.value)}
              className="px-6 py-3 rounded-lg bg-background border border-white/10 text-text-secondary outline-none focus:border-accent transition-colors"
            >
              <option value="Personal file sync">Personal file sync</option>
              <option value="Family sharing">Family sharing</option>
              <option value="My own machines">Work between my own machines</option>
              <option value="Just curious">Just curious</option>
            </select>
            <button
              type="submit"
              className="px-6 py-3 rounded-lg bg-accent text-black font-bold transition-transform hover:scale-105 active:scale-95"
            >
              Join the Pioneers →
            </button>
          </form>
        ) : (
          <div className="text-accent font-bold text-2xl animate-fade-in">
            You're in. We'll reach out when Pioneer Access opens.
          </div>
        )}
      </div>
    </section>
  );
};

export default PioneerAccess;
