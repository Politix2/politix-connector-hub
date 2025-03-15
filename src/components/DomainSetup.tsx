
import { useState } from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

// Mock function to generate topics based on domain
const generateTopicsForDomain = (domain: string): string[] => {
  // In a real app, this would call an API
  const topicsByDomain: Record<string, string[]> = {
    "energy": ["Energy Taxation", "Solar Subsidies", "Carbon Pricing", "Grid Infrastructure", "Renewable Targets"],
    "tech": ["Digital Infrastructure", "Data Privacy", "Platform Regulation", "AI Governance", "Cybersecurity"],
    "healthcare": ["Drug Pricing", "Healthcare Access", "Medical Data", "Insurance Reform", "Telehealth"],
    "finance": ["Banking Regulation", "Investment Rules", "Consumer Protection", "Digital Currencies", "Tax Policy"],
  };

  // Default to a mix of topics if domain isn't recognized
  const domainLower = domain.toLowerCase();
  
  for (const [key, topics] of Object.entries(topicsByDomain)) {
    if (domainLower.includes(key)) {
      return topics;
    }
  }
  
  return ["Energy Taxation", "Digital Infrastructure", "Market Competition", "Data Privacy", "Import/Export"];
};

interface DomainSetupProps {
  onComplete: (domain: string, topics: string[]) => void;
}

const DomainSetup = ({ onComplete }: DomainSetupProps) => {
  const [domain, setDomain] = useState("");
  const [step, setStep] = useState<"domain" | "topics">("domain");
  const [topics, setTopics] = useState<string[]>([]);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleDomainSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!domain) return;
    
    try {
      // In a real app, this would call your backend API
      // For now, we'll use our mock function
      const suggestedTopics = generateTopicsForDomain(domain);
      setTopics(suggestedTopics);
      setStep("topics");
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to suggest topics for your domain",
        variant: "destructive",
      });
    }
  };

  const handleComplete = () => {
    // Notify parent component
    onComplete(domain, topics);
    
    // Navigate to dashboard
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        {step === "domain" && (
          <>
            <CardHeader>
              <CardTitle className="text-2xl">Welcome to Regulatory Pulse</CardTitle>
              <CardDescription>
                Let's get started by understanding your industry
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleDomainSubmit}>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="domain" className="block text-sm font-medium text-gray-700 mb-1">
                      What industry is your organization in?
                    </label>
                    <Input
                      id="domain"
                      placeholder="e.g., Energy, Technology, Healthcare..."
                      value={domain}
                      onChange={(e) => setDomain(e.target.value)}
                      className="w-full"
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-politix-blue hover:bg-politix-dark">
                    Continue <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </form>
            </CardContent>
          </>
        )}

        {step === "topics" && (
          <>
            <CardHeader>
              <CardTitle className="text-2xl">Your Key Topics</CardTitle>
              <CardDescription>
                Based on your industry, we suggest monitoring these topics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topics.map((topic, index) => (
                  <div key={index} className="flex items-center p-3 border rounded-md">
                    <div className="font-medium">{topic}</div>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter>
              <Button 
                onClick={handleComplete} 
                className="w-full bg-politix-blue hover:bg-politix-dark"
              >
                Begin Monitoring
              </Button>
            </CardFooter>
          </>
        )}
      </Card>
    </div>
  );
};

export default DomainSetup;
