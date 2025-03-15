
import { Button } from "@/components/ui/button";
import { ArrowRight, BarChart2, PieChart, Globe } from "lucide-react";
import { Link } from "react-router-dom";

const Hero = () => {
  return (
    <div className="bg-gradient-to-r from-politix-blue to-politix-dark text-white py-20 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-10 md:mb-0 animate-slide-up">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
              Regulatory Pulse: Your Smart Public Affairs Companion
            </h1>
            <p className="text-lg md:text-xl mb-8 text-gray-200 max-w-lg">
              Stay ahead of political and legislative developments that impact your business with AI-powered insights and strategic guidance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                className="bg-white text-politix-blue hover:bg-gray-100 transition-colors text-base px-6 py-6"
                asChild
              >
                <Link to="/dashboard">
                  Launch Dashboard <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button 
                variant="outline" 
                className="border-white text-white hover:bg-white/10 transition-colors text-base px-6 py-6"
              >
                See How It Works
              </Button>
            </div>
          </div>
          <div className="md:w-1/2 flex justify-center animate-fade-in">
            <div className="relative">
              <div className="w-72 h-72 md:w-96 md:h-96 bg-white/10 rounded-full absolute blur-3xl"></div>
              <div className="relative flex items-center justify-center">
                <BarChart2 className="h-32 w-32 md:h-40 md:w-40 text-white" />
                <PieChart className="h-24 w-24 md:h-32 md:w-32 text-white absolute top-12 -right-10" />
                <Globe className="h-20 w-20 md:h-28 md:w-28 text-white absolute -bottom-8 -left-8" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
