import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ArrowRight,
  FileText,
  Sparkles,
  Target,
  Users,
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-10">
      <section className="text-center space-y-4 py-10">
        <div className="inline-flex items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs">
          <Sparkles className="h-3.5 w-3.5 text-primary" />
          NLP + Machine Learning
        </div>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
          Resume Screening, <span className="text-primary">automated.</span>
        </h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Upload resumes, paste a job description, and get instant ATS scores,
          ranked candidates, skill-gap analysis, and downloadable recruiter reports.
        </p>
        <div className="flex justify-center gap-3">
          <Link href="/dashboard">
            <Button size="lg">
              Open dashboard <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <Link href="/upload">
            <Button size="lg" variant="outline">
              Upload resumes
            </Button>
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-4">
        {[
          {
            icon: FileText,
            title: "Smart parsing",
            desc: "PDF & DOCX parsing with NER and contact extraction.",
          },
          {
            icon: Target,
            title: "ATS scoring",
            desc: "Composite score from skills, similarity, experience, education.",
          },
          {
            icon: Users,
            title: "Ranked candidates",
            desc: "Top matches surfaced automatically per job.",
          },
          {
            icon: Sparkles,
            title: "Recruiter reports",
            desc: "JSON + downloadable PDF reports with recommendations.",
          },
        ].map((f) => {
          const I = f.icon;
          return (
            <Card key={f.title}>
              <CardHeader>
                <div className="h-9 w-9 rounded-md bg-primary/10 text-primary flex items-center justify-center">
                  <I className="h-4 w-4" />
                </div>
                <CardTitle className="text-base">{f.title}</CardTitle>
                <CardDescription>{f.desc}</CardDescription>
              </CardHeader>
              <CardContent />
            </Card>
          );
        })}
      </section>
    </div>
  );
}
