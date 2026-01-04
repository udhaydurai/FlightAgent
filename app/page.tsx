import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 gap-8">
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>
      <h1 className="text-4xl font-bold">Flight Agent</h1>
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome</CardTitle>
          <CardDescription>Phase 1 setup complete</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input placeholder="Test input component" />
          <Button className="w-full">Test Button</Button>
        </CardContent>
      </Card>
    </main>
  );
}
