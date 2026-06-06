import React from 'react';

const ProblemSection = () => {
  const painPoints = [
    {
      title: "Pay monthly forever",
      description: "Stop paying for the privilege of storing your own data.",
      icon: "💸"
    },
    {
      title: "Your data on their servers",
      description: "Privacy isn't a setting, it's ownership. Own your hardware.",
      icon: "🛡️"
    },
    {
      title: "Limited Infrastructure",
      description: "Speed limited by their servers, not your local network.",
      icon: "🚀"
    }
  ];

  return (
    <section className="py-24 px-6 bg-background-secondary">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-brand font-bold text-center text-text-primary mb-16">
          You're renting access to <span className="text-accent">your own files.</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {painPoints.map((point, idx) => (
            <div key={idx} className="p-8 rounded-2xl bg-background border border-white/5 hover:border-accent/30 transition-colors group">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">
                {point.icon}
              </div>
              <h3 className="text-xl font-bold text-text-primary mb-3">{point.title}</h3>
              <p className="text-text-secondary font-body leading-relaxed">
                {point.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProblemSection;
