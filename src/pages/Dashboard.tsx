
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { ArrowUp, ArrowDown, BarChart, PieChart, TrendingUp, Users, List } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const Dashboard = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow bg-gray-50 py-8 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Political Dashboard</h1>
              <p className="text-gray-600">Visualize and analyze political data in real-time</p>
            </div>
            <div className="mt-4 md:mt-0 flex gap-2">
              <Button variant="outline" className="flex items-center gap-2">
                <List className="h-4 w-4" />
                Filters
              </Button>
              <Button className="bg-politix-blue hover:bg-politix-dark">
                Export Data
              </Button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Voter Turnout</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">67.3%</div>
                  <div className="flex items-center text-green-600">
                    <ArrowUp className="h-4 w-4 mr-1" />
                    <span className="text-sm">3.2%</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Compared to last election</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Party Support</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">Balanced</div>
                  <div className="flex items-center text-gray-600">
                    <TrendingUp className="h-4 w-4 mr-1" />
                    <span className="text-sm">Steady</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Major parties within 2% margin</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Policy Approval</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">52.8%</div>
                  <div className="flex items-center text-red-600">
                    <ArrowDown className="h-4 w-4 mr-1" />
                    <span className="text-sm">1.5%</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Average across major policies</p>
              </CardContent>
            </Card>
          </div>
          
          <Tabs defaultValue="overview" className="mb-8">
            <TabsList className="mb-6">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="demographics">Demographics</TabsTrigger>
              <TabsTrigger value="regions">Regions</TabsTrigger>
              <TabsTrigger value="issues">Key Issues</TabsTrigger>
            </TabsList>
            
            <TabsContent value="overview">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="col-span-1 min-h-[400px]">
                  <CardHeader>
                    <CardTitle>Political Landscape</CardTitle>
                    <CardDescription>Distribution of political affiliations</CardDescription>
                  </CardHeader>
                  <CardContent className="flex items-center justify-center">
                    <div className="text-center">
                      <PieChart className="h-40 w-40 mx-auto text-politix-blue opacity-30" />
                      <p className="mt-4 text-gray-500">Connect data sources to view charts</p>
                    </div>
                  </CardContent>
                </Card>
                
                <Card className="col-span-1 min-h-[400px]">
                  <CardHeader>
                    <CardTitle>Trending Issues</CardTitle>
                    <CardDescription>Most discussed political topics</CardDescription>
                  </CardHeader>
                  <CardContent className="flex items-center justify-center">
                    <div className="text-center">
                      <BarChart className="h-40 w-40 mx-auto text-politix-red opacity-30" />
                      <p className="mt-4 text-gray-500">Connect data sources to view charts</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
            
            <TabsContent value="demographics">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Demographic Analysis</CardTitle>
                  <CardDescription>Voting patterns by demographic groups</CardDescription>
                </CardHeader>
                <CardContent className="flex items-center justify-center">
                  <div className="text-center">
                    <Users className="h-40 w-40 mx-auto text-politix-blue opacity-30" />
                    <p className="mt-4 text-gray-500">Connect data sources to view demographic analysis</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="regions">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Regional Breakdown</CardTitle>
                  <CardDescription>Political trends by geographic regions</CardDescription>
                </CardHeader>
                <CardContent className="flex items-center justify-center">
                  <div className="text-center">
                    <BarChart className="h-40 w-40 mx-auto text-politix-red opacity-30" />
                    <p className="mt-4 text-gray-500">Connect data sources to view regional breakdown</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="issues">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Key Policy Issues</CardTitle>
                  <CardDescription>Public sentiment on major policy areas</CardDescription>
                </CardHeader>
                <CardContent className="flex items-center justify-center">
                  <div className="text-center">
                    <TrendingUp className="h-40 w-40 mx-auto text-politix-blue opacity-30" />
                    <p className="mt-4 text-gray-500">Connect data sources to view policy analysis</p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Dashboard;
