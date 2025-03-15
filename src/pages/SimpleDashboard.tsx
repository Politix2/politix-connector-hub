
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { FileText, MessageSquare, AlertTriangle } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import DomainSetup from "@/components/DomainSetup";

// Simulated data for the activity feed
const MOCK_PARLIAMENTARY_ACTIVITY = [
  {
    id: "p1",
    title: "Energy Taxation Bill (ETB-2023)",
    description: "Scheduled for debate tomorrow at 14:00",
    priority: "high",
    time: "2h ago",
    type: "parliament"
  },
  {
    id: "p2",
    title: "Digital Infrastructure Framework",
    description: "Committee review scheduled for Friday",
    priority: "medium",
    time: "5h ago",
    type: "parliament"
  }
];

const MOCK_SOCIAL_ACTIVITY = [
  {
    id: "s1",
    author: "@MinisterSchmidt",
    content: "We must accelerate our transition to renewable energy sources. The new taxation framework will help guide this change.",
    topic: "Energy Taxation",
    time: "3h ago",
    type: "tweet"
  },
  {
    id: "s2",
    author: "@DigitalCommittee",
    content: "Friday's meeting will focus on rural broadband access and 5G security protocols. Industry input welcome.",
    topic: "Digital Infrastructure",
    time: "4h ago",
    type: "tweet"
  }
];

const SimpleDashboard = () => {
  const [setupComplete, setSetupComplete] = useState(false);
  const [topics, setTopics] = useState<string[]>([]);
  const [activityFeed, setActivityFeed] = useState<any[]>([]);
  
  useEffect(() => {
    // Check if user has completed setup
    const savedTopics = localStorage.getItem("userTopics");
    
    if (savedTopics) {
      setTopics(JSON.parse(savedTopics));
      setSetupComplete(true);
      
      // Combine and sort mock data by time (newest first)
      const combinedActivity = [...MOCK_PARLIAMENTARY_ACTIVITY, ...MOCK_SOCIAL_ACTIVITY]
        .sort((a, b) => {
          const timeA = parseInt(a.time);
          const timeB = parseInt(b.time);
          return timeA - timeB;
        });
        
      setActivityFeed(combinedActivity);
    }
  }, []);
  
  const handleSetupComplete = (_domain: string, newTopics: string[]) => {
    setTopics(newTopics);
    setSetupComplete(true);
  };
  
  if (!setupComplete) {
    return <DomainSetup onComplete={handleSetupComplete} />;
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow bg-gray-50 py-8 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Regulatory Pulse</h1>
            <p className="text-gray-600">Monitoring your key regulatory topics</p>
          </div>
          
          {/* Topics Bar */}
          <div className="flex flex-wrap gap-2 mb-8 overflow-x-auto pb-2">
            {topics.map((topic, index) => (
              <div 
                key={index} 
                className="bg-white px-4 py-2 rounded-full border shadow-sm text-sm font-medium"
              >
                {topic}
              </div>
            ))}
          </div>
          
          {/* Critical Alert (if any) */}
          <Alert className="mb-6 border-amber-300 bg-amber-50">
            <AlertTriangle className="h-4 w-4 text-amber-600" />
            <AlertTitle className="text-amber-800">Critical Update</AlertTitle>
            <AlertDescription className="text-amber-700">
              New energy taxation bill scheduled for debate tomorrow in the German Parliament.
            </AlertDescription>
          </Alert>
          
          {/* Activity Feed */}
          <Card>
            <CardHeader>
              <CardTitle>Live Activity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {activityFeed.map((activity) => (
                  <div key={activity.id} className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 border-l-4 border-l-politix-blue">
                    {activity.type === "parliament" ? (
                      <FileText className="h-5 w-5 text-politix-blue mt-0.5" />
                    ) : (
                      <MessageSquare className="h-5 w-5 text-politix-blue mt-0.5" />
                    )}
                    <div className="flex-1">
                      <div className="flex justify-between">
                        <h4 className="font-medium">
                          {activity.type === "tweet" ? activity.author : activity.title}
                        </h4>
                        <span className="text-xs text-gray-500">{activity.time}</span>
                      </div>
                      <p className="text-sm text-gray-700 mt-1">
                        {activity.type === "tweet" ? activity.content : activity.description}
                      </p>
                      {activity.type === "tweet" && (
                        <div className="mt-1 text-xs text-politix-blue font-medium">
                          Topic: {activity.topic}
                        </div>
                      )}
                      {activity.type === "parliament" && activity.priority === "high" && (
                        <div className="mt-2">
                          <span className="text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">
                            High Priority
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default SimpleDashboard;
