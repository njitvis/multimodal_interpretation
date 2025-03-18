import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    output: "export",
    images: { unoptimized: true }, // Required for Next.js images
    typescript: {
      ignoreBuildErrors: true, // Ignores TS errors
    },
    webpack5: true,
    webpack: (config) => {
      config.resolve.fallback = { fs: false };
  
      return config;
    },
};

export default nextConfig;