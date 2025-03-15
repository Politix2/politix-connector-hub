
import { FileText, MessageSquare, Rss, Info, ArrowRight } from "lucide-react";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useQuery } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import { toast } from "@/components/ui/use-toast";

// Mock data for live activity
const MOCK_ACTIVITIES = [
  {
    id: 1,
    type: "parliament",
    title: "Energy Taxation Bill Debate",
    content: "Finance Committee discussing carbon pricing mechanisms and their impact on renewable energy producers.",
    date: new Date(2023, 5, 15),
    topics: ["Energy Taxation", "Carbon Pricing"],
    relevance: "This directly impacts your interest in energy taxation policies and may affect how solar electricity is taxed.",
    recommendation: "Contact the committee chair to schedule a briefing on how these changes would affect renewable energy production costs."
  },
  {
    id: 2,
    type: "tweet",
    author: "@GermanEnergyMin",
    content: "New solar subsidy program to be announced next week. Stay tuned for details on eligibility and application process.",
    date: new Date(2023, 5, 14),
    topics: ["Solar Subsidies", "Renewable Targets"],
    relevance: "This announcement aligns with your interest in continued EU subsidization of solar electricity.",
    recommendation: "Prepare documentation of your current projects to ensure quick application when the program launches."
  },
  {
    id: 3,
    type: "news",
    title: "EU Commission Publishes Draft Renewable Energy Directive",
    source: "EuroPolitics Daily",
    content: "New targets proposed for member states, with increased focus on solar and wind energy deployment.",
    date: new Date(2023, 5, 13),
    topics: ["Renewable Targets", "Energy Taxation"],
    relevance: "The directive includes provisions that may increase subsidies for solar electricity across the EU.",
    recommendation: "Review the draft directive and submit feedback during the public consultation period."
  },
  {
    id: 4,
    type: "parliament",
    title: "Digital Infrastructure Committee Hearing",
    content: "Discussion on broadband deployment in rural areas and 5G network security requirements.",
    date: new Date(2023, 5, 12),
    topics: ["Digital Infrastructure"],
    relevance: "This hearing covers regulatory aspects of digital infrastructure that may affect your operations.",
    recommendation: "Monitor the committee's recommendations, as they may lead to new compliance requirements."
  },
  {
    id: 5,
    type: "tweet",
    author: "@EUCompetition",
    content: "We're launching an investigation into market practices in the energy sector, focusing on fair competition among renewable providers.",
    date: new Date(2023, 5, 11),
    topics: ["Market Competition", "Energy Taxation"],
    relevance: "This investigation could affect competitive dynamics in the renewable energy market.",
    recommendation: "Review your market pricing strategies and prepare documentation of your competitive practices."
  }
];

interface LiveActivityProps {
  topics: string[];
}

const LiveActivity = ({ topics }: LiveActivityProps) => {
  const [activities, setActivities] = useState<typeof MOCK_ACTIVITIES>([]);

  // Simulate fetching activities from an API
  const { data, isLoading } = useQuery({
    queryKey: ['activities', topics],
    queryFn: async () => {
      // In a real app, this would be a fetch call to your backend
      // For now, we'll filter the mock data based on the topics
      return new Promise(resolve => {
        setTimeout(() => {
          const filteredActivities = MOCK_ACTIVITIES.filter(activity => 
            activity.topics.some(topic => topics.includes(topic))
          );
          resolve(filteredActivities);
        }, 500);
      });
    }
  });

  useEffect(() => {
    if (data) {
      setActivities(data as typeof MOCK_ACTIVITIES);
    }
  }, [data]);

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'parliament':
        return <FileText className="h-5 w-5 text-blue-600" />;
      case 'tweet':
        return <MessageSquare className="h-5 w-5 text-sky-400" />;
      case 'news':
        return <Rss className="h-5 w-5 text-orange-500" />;
      default:
        return <Info className="h-5 w-5" />;
    }
  };

  const getActivityTypeName = (type: string) => {
    switch (type) {
      case 'parliament':
        return 'Parliamentary Debate';
      case 'tweet':
        return 'X Post';
      case 'news':
        return 'RSS News';
      default:
        return 'Activity';
    }
  };

  if (isLoading) {
    return <p className="text-center py-8">Loading activities...</p>;
  }

  if (activities.length === 0) {
    return (
      <Card className="w-full my-4">
        <CardContent className="pt-6 text-center">
          <p className="text-muted-foreground">No activities found for your topics.</p>
          <p className="text-sm text-muted-foreground mt-2">Try adding more topics to see relevant activities.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4 my-4">
      <h2 className="text-xl font-semibold">Live Activity</h2>
      {activities.map((activity) => (
        <Card key={activity.id} className="w-full">
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <div className="mt-1">{getActivityIcon(activity.type)}</div>
              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <div>
                    <Badge variant="outline" className="mb-2">
                      {getActivityTypeName(activity.type)}
                    </Badge>
                    <h3 className="font-medium text-lg">
                      {activity.type === 'tweet' ? `Tweet from ${activity.author}` : activity.title}
                    </h3>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {activity.date.toLocaleDateString()}
                  </span>
                </div>
                <p className="text-sm mt-1">{activity.content}</p>
                
                <div className="mt-4 space-y-2">
                  <div className="bg-muted p-3 rounded-md">
                    <h4 className="text-sm font-medium">Why this is relevant:</h4>
                    <p className="text-sm mt-1 text-muted-foreground">{activity.relevance}</p>
                  </div>
                  
                  <div className="bg-blue-50 p-3 rounded-md">
                    <h4 className="text-sm font-medium text-blue-700">Recommendation:</h4>
                    <p className="text-sm mt-1 text-blue-600">{activity.recommendation}</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="border-t pt-4 flex justify-end">
            <Button variant="outline" size="sm" className="mr-2">Dismiss</Button>
            <Button size="sm" className="bg-politix-blue hover:bg-politix-dark text-white">
              Take Action <ArrowRight className="ml-2 h-3.5 w-3.5" />
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
};

export default LiveActivity;
