"use client";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { ScoreRadar } from "@/components/dashboard/score-radar";
import { cn, scoreColor } from "@/lib/utils";
import { api } from "@/lib/api";
import type { ScreeningReport } from "@/lib/types";
import { Download, Mail, Phone, Briefcase, GraduationCap } from "lucide-react";

interface Props {
  data: ScreeningReport;
}

export function ReportView({ data }: Props) {
  const { screening: s, resume: r, job: j, report } = data;
  const radarData = [
    { metric: "Skills", score: s.skill_match },
    { metric: "Similarity", score: s.similarity * 100 },
    { metric: "Keywords", score: s.keyword_match },
    { metric: "Experience", score: s.experience_match },
    { metric: "Education", score: s.education_match },
  ];

  const verdictVariant: Record<string, "success" | "default" | "warn" | "danger"> = {
    "Strong Match": "success",
    "Good Match": "default",
    Borderline: "warn",
    "Weak Match": "danger",
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">
            {r.candidate_name || r.file_name}
          </h1>
          <p className="text-sm text-muted-foreground">
            Screened against <span className="font-medium">{j.title}</span>
            {j.company ? ` at ${j.company}` : ""}
          </p>
        </div>
        <a href={api.reportPdfUrl(s.id)} target="_blank" rel="noreferrer">
          <Button>
            <Download className="h-4 w-4" />
            Download PDF
          </Button>
        </a>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">ATS Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end gap-2">
              <div className={cn("text-5xl font-bold", scoreColor(s.ats_score))}>
                {s.ats_score.toFixed(1)}
              </div>
              <div className="text-muted-foreground mb-1">/ 100</div>
            </div>
            <Progress value={s.ats_score} className="mt-3" />
            <div className="mt-3">
              <Badge variant={verdictVariant[report.verdict] || "default"}>
                {report.verdict}
              </Badge>
            </div>

            <Separator className="my-4" />

            <div className="space-y-2 text-sm">
              {r.email ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Mail className="h-3.5 w-3.5" />
                  {r.email}
                </div>
              ) : null}
              {r.phone ? (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Phone className="h-3.5 w-3.5" />
                  {r.phone}
                </div>
              ) : null}
              <div className="flex items-center gap-2 text-muted-foreground">
                <Briefcase className="h-3.5 w-3.5" />
                {r.experience_years} years experience
              </div>
              <div className="flex items-center gap-2 text-muted-foreground">
                <GraduationCap className="h-3.5 w-3.5" />
                {r.education.length
                  ? r.education.slice(0, 3).join(", ")
                  : "No education extracted"}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Score breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <ScoreRadar data={radarData} />
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-sm">
              {radarData.map((d) => (
                <div key={d.metric} className="rounded-md border p-3">
                  <div className="text-muted-foreground text-xs">{d.metric}</div>
                  <div className={cn("font-semibold text-lg", scoreColor(d.score))}>
                    {d.score.toFixed(1)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Matched skills</CardTitle>
          </CardHeader>
          <CardContent>
            {s.matched_skills.length ? (
              <div className="flex flex-wrap gap-2">
                {s.matched_skills.map((sk) => (
                  <Badge key={sk} variant="success">{sk}</Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No required skills matched.</p>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Skill gap</CardTitle>
          </CardHeader>
          <CardContent>
            {s.missing_skills.length ? (
              <div className="flex flex-wrap gap-2">
                {s.missing_skills.map((sk) => (
                  <Badge key={sk} variant="danger">{sk}</Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">No skill gaps detected. Great fit!</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc pl-5 text-sm space-y-1">
            {report.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
