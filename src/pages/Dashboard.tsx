
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { 
  ArrowUp, ArrowDown, BarChart, PieChart, TrendingUp, Users, List, 
  Bell, AlertTriangle, MessageSquare, FileText, Zap 
} from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const Dashboard = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow bg-gray-50 py-8 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Regulatory Pulse</h1>
              <p className="text-gray-600">Monitor and respond to legislative developments</p>
            </div>
            <div className="mt-4 md:mt-0 flex gap-2">
              <Button variant="outline" className="flex items-center gap-2">
                <List className="h-4 w-4" />
                Topics
              </Button>
              <Button className="bg-politix-blue hover:bg-politix-dark">
                Add New Topic
              </Button>
            </div>
          </div>
          
          <Alert className="mb-6 border-amber-300 bg-amber-50">
            <AlertTriangle className="h-4 w-4 text-amber-600" />
            <AlertTitle className="text-amber-800">Critical Update</AlertTitle>
            <AlertDescription className="text-amber-700">
              New energy taxation bill scheduled for debate tomorrow in the German Parliament.
            </AlertDescription>
          </Alert>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Active Topics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">7</div>
                  <div className="flex items-center text-green-600">
                    <ArrowUp className="h-4 w-4 mr-1" />
                    <span className="text-sm">New</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Topics currently being monitored</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Alerts Today</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">12</div>
                  <div className="flex items-center text-amber-600">
                    <Bell className="h-4 w-4 mr-1" />
                    <span className="text-sm">3 Urgent</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Developments requiring attention</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">Engagement Opportunities</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="text-2xl font-bold">5</div>
                  <div className="flex items-center text-blue-600">
                    <MessageSquare className="h-4 w-4 mr-1" />
                    <span className="text-sm">Action Needed</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">Recommended stakeholder engagements</p>
              </CardContent>
            </Card>
          </div>
          
          <Tabs defaultValue="monitoring" className="mb-8">
            <TabsList className="mb-6">
              <TabsTrigger value="monitoring">Live Monitoring</TabsTrigger>
              <TabsTrigger value="topics">Key Topics</TabsTrigger>
              <TabsTrigger value="alerts">Smart Alerts</TabsTrigger>
              <TabsTrigger value="engagement">Engagement</TabsTrigger>
            </TabsList>
            
            <TabsContent value="monitoring">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="col-span-1 min-h-[400px]">
                  <CardHeader>
                    <CardTitle>Parliamentary Activity</CardTitle>
                    <CardDescription>Live debates and upcoming votes</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-start gap-3 p-3 rounded-lg bg-gray-50">
                        <FileText className="h-5 w-5 text-politix-blue mt-0.5" />
                        <div>
                          <h4 className="font-medium">Energy Taxation Bill (ETB-2023)</h4>
                          <p className="text-sm text-gray-500">Scheduled for debate tomorrow at 14:00</p>
                          <div className="flex items-center mt-2">
                            <span className="text-xs bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">High Priority</span>
                            <span className="text-xs text-gray-500 ml-auto">Updated 2h ago</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-start gap-3 p-3 rounded-lg bg-gray-50">
                        <FileText className="h-5 w-5 text-politix-blue mt-0.5" />
                        <div>
                          <h4 className="font-medium">Digital Infrastructure Framework</h4>
                          <p className="text-sm text-gray-500">Committee review scheduled for Friday</p>
                          <div className="flex items-center mt-2">
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">Medium Priority</span>
                            <span className="text-xs text-gray-500 ml-auto">Updated 5h ago</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-start gap-3 p-3 rounded-lg bg-gray-50">
                        <FileText className="h-5 w-5 text-politix-blue mt-0.5" />
                        <div>
                          <h4 className="font-medium">Solar Subsidy Program</h4>
                          <p className="text-sm text-gray-500">Final reading scheduled next week</p>
                          <div className="flex items-center mt-2">
                            <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">Watch</span>
                            <span className="text-xs text-gray-500 ml-auto">Updated 1d ago</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card className="col-span-1 min-h-[400px]">
                  <CardHeader>
                    <CardTitle>Public Sentiment</CardTitle>
                    <CardDescription>Social media and news analysis</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center pb-4 mb-4 border-b">
                      <div className="flex justify-between items-center mb-4">
                        <span className="text-sm text-gray-500">Topic:</span>
                        <Select defaultValue="energy">
                          <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select topic" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="energy">Energy Taxation</SelectItem>
                            <SelectItem value="digital">Digital Infrastructure</SelectItem>
                            <SelectItem value="solar">Solar Subsidies</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="flex justify-center gap-6 text-center">
                        <div>
                          <div className="text-3xl font-bold text-green-600">64%</div>
                          <div className="text-xs text-gray-500">Positive</div>
                        </div>
                        <div>
                          <div className="text-3xl font-bold text-gray-500">21%</div>
                          <div className="text-xs text-gray-500">Neutral</div>
                        </div>
                        <div>
                          <div className="text-3xl font-bold text-red-600">15%</div>
                          <div className="text-xs text-gray-500">Negative</div>
                        </div>
                      </div>
                    </div>
                    <div className="space-y-3">
                      <div className="flex gap-2 items-center text-sm">
                        <Zap className="h-4 w-4 text-amber-500" />
                        <span>Trending keywords: "sustainable", "fair", "transition"</span>
                      </div>
                      <div className="flex gap-2 items-center text-sm">
                        <Users className="h-4 w-4 text-blue-500" />
                        <span>42 key influencers engaged in discussion</span>
                      </div>
                      <div className="flex gap-2 items-center text-sm">
                        <TrendingUp className="h-4 w-4 text-green-500" />
                        <span>137% increase in public discourse since last week</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
            
            <TabsContent value="topics">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Monitored Topics</CardTitle>
                  <CardDescription>Your selected regulatory areas of interest</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Energy Taxation</h3>
                        <p className="text-sm text-gray-500">Changes to carbon taxes and incentives</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-700">
                        Urgent
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Digital Infrastructure</h3>
                        <p className="text-sm text-gray-500">5G rollout and tech regulations</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                        Active
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Solar Subsidies</h3>
                        <p className="text-sm text-gray-500">Renewable energy incentive programs</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">
                        Stable
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Market Competition</h3>
                        <p className="text-sm text-gray-500">Antitrust and fair practice laws</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-700">
                        Developing
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Data Privacy</h3>
                        <p className="text-sm text-gray-500">GDPR and data protection updates</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                        Active
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Labor Laws</h3>
                        <p className="text-sm text-gray-500">Employment regulations and reforms</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-700">
                        Quiet
                      </span>
                    </div>
                    
                    <div className="border rounded-md p-4 flex justify-between hover:bg-gray-50 transition-colors">
                      <div>
                        <h3 className="font-medium">Import/Export</h3>
                        <p className="text-sm text-gray-500">Trade agreements and tariffs</p>
                      </div>
                      <span className="inline-flex h-6 items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-700">
                        Quiet
                      </span>
                    </div>
                    
                    <Button variant="outline" className="border-dashed border-2 h-full py-6 flex flex-col gap-2">
                      <span className="text-base font-normal">Add New Topic</span>
                      <span className="text-xs text-gray-500">Monitor additional regulatory areas</span>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="alerts">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Smart Alerts</CardTitle>
                  <CardDescription>AI-generated insights and notifications</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="border-l-4 border-red-500 pl-4 py-2 bg-red-50 rounded-r-md">
                      <div className="flex justify-between">
                        <h3 className="font-medium">Energy Taxation Bill</h3>
                        <span className="text-xs text-gray-500">2h ago</span>
                      </div>
                      <p className="text-sm mt-1">Finance Minister has publicly announced support for increased carbon pricing, contradicting earlier position papers.</p>
                      <div className="mt-2 flex gap-2">
                        <Button variant="outline" size="sm" className="text-xs h-7">View Analysis</Button>
                        <Button size="sm" className="text-xs h-7 bg-politix-blue">Engagement Plan</Button>
                      </div>
                    </div>
                    
                    <div className="border-l-4 border-amber-500 pl-4 py-2 bg-amber-50 rounded-r-md">
                      <div className="flex justify-between">
                        <h3 className="font-medium">Digital Infrastructure</h3>
                        <span className="text-xs text-gray-500">5h ago</span>
                      </div>
                      <p className="text-sm mt-1">Committee chairman requested industry input on 5G security protocols ahead of Friday's meeting.</p>
                      <div className="mt-2 flex gap-2">
                        <Button variant="outline" size="sm" className="text-xs h-7">View Details</Button>
                        <Button size="sm" className="text-xs h-7 bg-politix-blue">Prepare Statement</Button>
                      </div>
                    </div>
                    
                    <div className="border-l-4 border-blue-500 pl-4 py-2 bg-blue-50 rounded-r-md">
                      <div className="flex justify-between">
                        <h3 className="font-medium">Solar Subsidies</h3>
                        <span className="text-xs text-gray-500">1d ago</span>
                      </div>
                      <p className="text-sm mt-1">Three major newspapers published editorial support for expanded solar subsidy programs.</p>
                      <div className="mt-2 flex gap-2">
                        <Button variant="outline" size="sm" className="text-xs h-7">View Analysis</Button>
                      </div>
                    </div>
                    
                    <div className="border-l-4 border-gray-300 pl-4 py-2 bg-gray-50 rounded-r-md">
                      <div className="flex justify-between">
                        <h3 className="font-medium">Labor Law Reform</h3>
                        <span className="text-xs text-gray-500">2d ago</span>
                      </div>
                      <p className="text-sm mt-1">Opposition party announced plans to propose amendments to work-from-home regulations.</p>
                      <div className="mt-2 flex gap-2">
                        <Button variant="outline" size="sm" className="text-xs h-7">Monitor</Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="engagement">
              <Card className="min-h-[400px]">
                <CardHeader>
                  <CardTitle>Engagement Guidance</CardTitle>
                  <CardDescription>Strategic recommendations for stakeholder outreach</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="border rounded-lg p-4">
                      <h3 className="font-medium text-lg mb-2">Energy Taxation Bill Response</h3>
                      <p className="text-sm text-gray-600 mb-4">Recommended actions based on latest parliamentary developments</p>
                      
                      <div className="space-y-3">
                        <div className="flex items-start gap-3">
                          <Users className="h-5 w-5 text-politix-blue mt-0.5" />
                          <div>
                            <h4 className="font-medium">Key Stakeholders</h4>
                            <ul className="text-sm text-gray-600 mt-1 list-disc list-inside">
                              <li>Finance Committee Chair (Dr. Schmidt)</li>
                              <li>Industry Association Representatives</li>
                              <li>Economic Ministry Liaison</li>
                            </ul>
                          </div>
                        </div>
                        
                        <div className="flex items-start gap-3">
                          <MessageSquare className="h-5 w-5 text-politix-blue mt-0.5" />
                          <div>
                            <h4 className="font-medium">Messaging Strategy</h4>
                            <p className="text-sm text-gray-600 mt-1">
                              Emphasize economic impact analysis and transition timeline concerns while acknowledging climate goals.
                            </p>
                          </div>
                        </div>
                        
                        <div className="flex items-start gap-3">
                          <FileText className="h-5 w-5 text-politix-blue mt-0.5" />
                          <div>
                            <h4 className="font-medium">Documentation</h4>
                            <p className="text-sm text-gray-600 mt-1">
                              Prepare one-page briefing and detailed position paper with industry data.
                            </p>
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-4 pt-4 border-t flex justify-end">
                        <Button className="bg-politix-blue">Begin Engagement Process</Button>
                      </div>
                    </div>
                    
                    <div className="border rounded-lg p-4">
                      <h3 className="font-medium text-lg mb-2">Digital Infrastructure Coalition</h3>
                      <p className="text-sm text-gray-600 mb-4">Form industry alliance to address upcoming regulatory changes</p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="border rounded p-3">
                          <h4 className="font-medium text-sm mb-1">Potential Partners</h4>
                          <p className="text-xs text-gray-500">12 companies identified</p>
                        </div>
                        
                        <div className="border rounded p-3">
                          <h4 className="font-medium text-sm mb-1">Policy Framework</h4>
                          <p className="text-xs text-gray-500">Draft completed (80%)</p>
                        </div>
                        
                        <div className="border rounded p-3">
                          <h4 className="font-medium text-sm mb-1">Launch Timeline</h4>
                          <p className="text-xs text-gray-500">2 weeks remaining</p>
                        </div>
                      </div>
                      
                      <div className="mt-4 pt-4 border-t flex justify-end">
                        <Button variant="outline" className="mr-2">View Details</Button>
                        <Button className="bg-politix-blue">Continue Setup</Button>
                      </div>
                    </div>
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
