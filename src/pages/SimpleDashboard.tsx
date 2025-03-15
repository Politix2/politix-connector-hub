
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import DomainSetup from "@/components/DomainSetup";
import TopicManagement from "@/components/TopicManagement";
import LiveActivity from "@/components/LiveActivity";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";

interface Topic {
  name: string;
  description: string;
}

const SimpleDashboard = () => {
  const [setupComplete, setSetupComplete] = useState(false);
  const [topics, setTopics] = useState<Topic[]>([]);
  const navigate = useNavigate();
  const { toast } = useToast();
  
  useEffect(() => {
    // Check if user has completed setup
    const savedTopics = localStorage.getItem("userTopics");
    if (savedTopics) {
      try {
        // Convert string topics to Topic objects with descriptions
        const parsedTopics = JSON.parse(savedTopics);
        const topicsWithDescriptions: Topic[] = Array.isArray(parsedTopics) 
          ? parsedTopics.map((topic: string | Topic) => {
              // If the saved topic is already a Topic object
              if (typeof topic === 'object' && topic !== null) {
                return topic;
              }
              // If it's just a string, convert it to a Topic object
              return { name: topic, description: "" };
            })
          : [];
        
        setTopics(topicsWithDescriptions);
        setSetupComplete(true);
      } catch (error) {
        console.error("Error parsing saved topics:", error);
        setSetupComplete(false);
      }
    } else {
      setSetupComplete(false);
    }
  }, []);
  
  const handleSetupComplete = (domain: string, selectedTopics: string[]) => {
    // Convert string topics to Topic objects
    const topicsWithDescriptions = selectedTopics.map(topic => ({
      name: topic,
      description: ""
    }));
    
    setTopics(topicsWithDescriptions);
    setSetupComplete(true);
    
    // Save to localStorage
    localStorage.setItem("userDomain", domain);
    localStorage.setItem("userTopics", JSON.stringify(topicsWithDescriptions));
    
    toast({
      title: "Setup complete!",
      description: `We'll monitor ${selectedTopics.length} topics for your organization.`,
    });
  };

  const handleUpdateTopics = (updatedTopics: Topic[]) => {
    setTopics(updatedTopics);
    localStorage.setItem("userTopics", JSON.stringify(updatedTopics));
  };

  const handleReset = () => {
    localStorage.removeItem("userDomain");
    localStorage.removeItem("userTopics");
    setSetupComplete(false);
    setTopics([]);
    toast({
      title: "Setup reset",
      description: "You can now start fresh with a new domain and topics.",
    });
  };
  
  if (!setupComplete) {
    return <DomainSetup onComplete={handleSetupComplete} />;
  }
  
  // Extract just the topic names for components that only need the names
  const topicNames = topics.map(topic => topic.name);

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow bg-gray-50 py-8 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Regulatory Pulse</h1>
              <p className="text-gray-600">Monitor and respond to legislative developments</p>
            </div>
            <div className="mt-4 md:mt-0">
              <Button variant="outline" className="text-sm" onClick={handleReset}>
                Reset Setup
              </Button>
            </div>
          </div>
          
          {/* Topic Management Section */}
          <TopicManagement topics={topics} onUpdateTopics={handleUpdateTopics} />
          
          {/* Live Activity Feed */}
          <LiveActivity topics={topicNames} />
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default SimpleDashboard;
