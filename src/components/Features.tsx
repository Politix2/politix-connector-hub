
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart2, PieChart, TrendingUp, Users, Database, Shield } from "lucide-react";

const features = [
  {
    icon: <BarChart2 className="h-10 w-10 text-politix-blue" />,
    title: "Interactive Charts",
    description: "Explore political data through interactive and dynamic visualizations."
  },
  {
    icon: <PieChart className="h-10 w-10 text-politix-red" />,
    title: "Demographic Analysis",
    description: "Understand voter demographics and political preferences across regions."
  },
  {
    icon: <TrendingUp className="h-10 w-10 text-politix-blue" />,
    title: "Trend Tracking",
    description: "Monitor political trends and shifts in public opinion over time."
  },
  {
    icon: <Users className="h-10 w-10 text-politix-red" />,
    title: "Voter Insights",
    description: "Gain insights into voter behavior and political engagement patterns."
  },
  {
    icon: <Database className="h-10 w-10 text-politix-blue" />,
    title: "Comprehensive Data",
    description: "Access a rich database of political information from reliable sources."
  },
  {
    icon: <Shield className="h-10 w-10 text-politix-red" />,
    title: "Unbiased Analysis",
    description: "Get politically neutral analysis based purely on factual data."
  }
];

const Features = () => {
  return (
    <section id="features" className="py-20 px-6 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-politix-dark">Powerful Features</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover how PolitiX helps you make sense of the complex political landscape.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="border border-gray-200 hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="mb-2">{feature.icon}</div>
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
