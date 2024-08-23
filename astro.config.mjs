import { defineConfig } from "astro/config";

import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind(), icon()],
  redirects: {
    bs: "https://docs.google.com/document/d/1btchpM25g_A4Z2Ij9pktgvqwrZ8OjI7acKCE8VjhzZM",
    os: "https://docs.google.com/document/d/1YTpdIXS3pSIuqgzjpocQvF3IMKqnK24I",
    cv: "https://drive.google.com/open?id=1BtjjVklNLArVmwvM-sANdpBtJz6_KPx61voC7kIWC6A",
    bio: "https://drive.google.com/open?id=1QEC5t9mQf17MR1C4LUTGmR9BZhzl62EFFDQs3Un0m6A",
    citi: "https://drive.google.com/open?id=0BxGOaSqlnUIAZThMNUU1Tm4wMk1wUW1KNURONDZSM2ExblZZ",
    pi2023:
      "https://docs.google.com/document/d/1Mhrki03XIVWRzCebxtl9BozyhSsLdXyLXSCCx43NVGc/",
    // ^/?pi20(.*)$ /presentations/Proteomics_Informatics_20$1
    methods2022:
      "https://docs.google.com/document/d/18fxsIdCZG11dDFKnX2CshRLiIyEsqpLlU8dqRBWiC7k/edit?usp=drive_link",
    methods2023:
      "https://docs.google.com/document/d/1JF5vFSGUMPyJm549UFBRlix6iCFqcCpCYryISgAdKNo",
    // ^/?methods20(.*)$ /presentations/Methods_20$1
    ml2022:
      "https://docs.google.com/document/d/1a3o-gTfq9wOnB-Lf3YhUbK6nUx_U1QYNxgKGJEoz-hM",
    ml2023:
      "https://docs.google.com/document/d/1eqMz6qzNsc-OawBYlzOWbf8z2Pr92qFH-PvVkyDHipE/",
    // ^/?ml20(.*)$ /presentations/Machine_Learning_20$1
  },
});
