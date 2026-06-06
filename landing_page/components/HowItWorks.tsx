import React from 'react';

const HowItWorks = () => {
  const steps = [
    {
      number: "01",
      title: "Install ShulkerBox",
      description: "Download the app on your PC. It sets up a private secure gateway in seconds."
    },
    {
      number: "02",
      title: "Add your devices",
      description: "Join your devices to your Tailscale network. They now speak a private language."
    },
    {
      number: "03",
      title: "Access everything",
      description: "Browse and transfer files instantly, anywhere in the world, privately."
    }
  ];

  return (
    <section className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-brand font-bold text-center text-text-primary mb-16">
          How it Works
        </h2>

        <div className="relative grid grid-cols-1 md:grid-cols-3 gap-12">
          {/* Desktop line connector */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-px bg-white/10 -translate-y-1/2 z-0" />

          {steps.map((step, idx) => (
            <div key={idx} className="relative z-10 flex flex-col items-center text-center">
              <div className="w-12 h-12 rounded-full bg-accent text-black font-brand font-bold flex items-center justify-center mb-6 shadow-[0_0_20px_rgba(245,166,35,0.4)]">
                {step.number}
              </div>
              <h3 className="text-xl font-bold text-text-primary mb-3">{step.title}</h3>
              <p className="text-text-secondary font-body">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
