
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight, CheckCircle, Loader2 } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { Progress } from "@/components/ui/progress";
import Navbar from "@/components/Navbar";

// Mock function to generate topics based on email domain
const generateTopicsForEmail = (email: string): string[] => {
  // In a real app, this would call an API
  const emailDomain = email.split('@')[1]?.split('.')[0] || '';
  
  const topicsByDomain: Record<string, string[]> = {
    "energy": ["Energy Taxation", "Solar Subsidies", "Carbon Pricing", "Grid Infrastructure", "Renewable Targets"],
    "tech": ["Digital Infrastructure", "Data Privacy", "Platform Regulation", "AI Governance", "Cybersecurity"],
    "healthcare": ["Drug Pricing", "Healthcare Access", "Medical Data", "Insurance Reform", "Telehealth"],
    "finance": ["Banking Regulation", "Investment Rules", "Consumer Protection", "Digital Currencies", "Tax Policy"],
  };

  // Default to a mix of topics if domain isn't recognized
  const domainLower = emailDomain.toLowerCase();
  
  for (const [key, topics] of Object.entries(topicsByDomain)) {
    if (domainLower.includes(key)) {
      return topics;
    }
  }
  
  return ["Energy Taxation", "Digital Infrastructure", "Market Competition", "Data Privacy", "Import/Export"];
};

const EmailEntry = () => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [step, setStep] = useState<"input" | "loading" | "complete">("input");
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      toast({
        title: "Invalid email",
        description: "Please enter a valid work email address",
        variant: "destructive",
      });
      return;
    }
    
    setLoading(true);
    setStep("loading");
    
    // Simulate progress steps
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          return 100;
        }
        return prev + 5;
      });
    }, 150);
    
    // Simulate API call
    setTimeout(() => {
      try {
        const suggestedTopics = generateTopicsForEmail(email);
        
        // Convert topics to topic objects with descriptions
        const topicsWithDescriptions = suggestedTopics.map(topic => ({
          name: topic,
          description: ""
        }));
        
        // Save to localStorage
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userTopics", JSON.stringify(topicsWithDescriptions));
        
        setStep("complete");
        clearInterval(progressInterval);
        setProgress(100);
        
        // Navigate after showing completion state briefly
        setTimeout(() => {
          navigate("/dashboard");
        }, 1500);
        
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to set up your regulatory pulse",
          variant: "destructive",
        });
        setLoading(false);
        setStep("input");
      }
    }, 3000);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <div className="flex-grow flex items-center justify-center bg-gray-50 p-4">
        <Card className="w-full max-w-md">
          {step === "input" && (
            <>
              <CardHeader>
                <CardTitle className="text-2xl">Welcome to Regulatory Pulse</CardTitle>
                <CardDescription>
                  Enter your work email to start monitoring relevant political topics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleEmailSubmit}>
                  <div className="space-y-4">
                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Work Email
                      </label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="your.name@company.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full"
                        required
                      />
                    </div>
                    <Button 
                      type="submit" 
                      className="w-full bg-politix-blue hover:bg-politix-dark"
                      disabled={loading}
                    >
                      Get Started <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </div>
                </form>
              </CardContent>
            </>
          )}

          {step === "loading" && (
            <>
              <CardHeader>
                <CardTitle className="text-2xl">Setting up your Regulatory Pulse</CardTitle>
                <CardDescription>
                  We're analyzing your organization to find relevant topics
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex justify-center my-8">
                  <Loader2 className="h-12 w-12 text-politix-blue animate-spin" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Analyzing domain</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
              </CardContent>
            </>
          )}

          {step === "complete" && (
            <>
              <CardHeader>
                <CardTitle className="text-2xl">Setup Complete!</CardTitle>
                <CardDescription>
                  Your Regulatory Pulse is ready
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center py-8">
                <CheckCircle className="h-16 w-16 text-green-500 mb-4" />
                <p className="text-center text-gray-600">
                  We've set up monitoring for topics relevant to your organization.
                </p>
              </CardContent>
            </>
          )}
        </Card>
      </div>
    </div>
  );
};

export default EmailEntry;
