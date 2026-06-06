import React from 'react';

const FeaturesSection = () => {
  const features = [
    {
      title: "Zero Setup",
      description: "Install and go. No router config, no port forwarding, no IT degree needed.",
      icon: "🔌"
    },
    {
      title: "End-to-End Encrypted",
      description: "WireGuard encryption. Your files never touch a third-party server.",
      icon: "🔒"
    },
    {
      title: "No Subscription",
      description: "Free forever. Self-hosted. The only cost is your own hardware.",
      icon: "🚫"
    },
    {
      title: "Works Everywhere",
      description: "PC to PC. PC to phone. Home network or across the world.",
      icon: "🌐"
    }
  ];

  return (
    <section className="py-24 px-6 bg-background-secondary">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-brand font-bold text-center text-text-primary mb-16">
          Built for Privacy. <span className="text-accent">Built for Humans.</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, idx) => (
            <div key={idx} className="p-8 rounded-2xl bg-background border border-white/5 hover:border-accent/30 transition-all group">
              <div className="flex items-center gap-4 mb-4">
                <span className="text-3xl group-hover:scale-110 transition-transform">{feature.icon}</span>
                <h3 className="text-xl font-bold text-text-primary">{feature.title}</h3>
              </div>
              <p className="text-text-secondary font-body leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
