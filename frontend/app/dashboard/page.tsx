"use client";
import * as React from "react";
import {
  BarChart3,
  Briefcase,
  FileText,
  Gauge,
  Sparkles,
  Users,
} from "lucide-react";
import { toast } from "sonner";

import { MetricCard } from "@/components/dashboard/metric-card";
import { ScoreDistributionChart } from "@/components/dashboard/score-distribution-chart";
import { TopSkillsChart } from "@/components/dashboard/top-skills-chart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import type {
  AnalyticsSummary,
  ScoreBucket,
  SkillCount,
} from "@/lib/types";

export default function DashboardPage() {
  const [summary, setSummary] = React.useState<AnalyticsSummary | null>(null);
  const [dist, setDist] = React.useState<ScoreBucket[]>([]);
  const [skills, setSkills] = React.useState<SkillCount[]>([]);

  React.useEffect(() => {
    (async () => {
      try {
        const [s, d, t] = await Promise.all([
          api.summary(),
          api.scoreDist(),
          api.topSkills(12),
        ]);
        setSummary(s);
        setDist(d);
        setSkills(t);
      } catch (e) {
        toast.error((e as Error).message);
      }
    })();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Overview of resumes, jobs, and screening results.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="Resumes"
          value={summary?.resumes ?? 0}
          icon={FileText}
          hint="Uploaded resumes"
        />
        <MetricCard
          label="Jobs"
          value={summary?.jobs ?? 0}
          icon={Briefcase}
          hint="Job descriptions saved"
        />
        <MetricCard
          label="Screenings"
          value={summary?.screenings ?? 0}
          icon={Users}
          hint="Resume × job matchings"
        />
        <MetricCard
          label="Avg ATS score"
          value={(summary?.avg_ats_score ?? 0).toFixed(1)}
          icon={Gauge}
          hint="Across all screenings"
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-primary" />
              ATS score distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScoreDistributionChart data={dist} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" />
              Top skills in resume pool
            </CardTitle>
          </CardHeader>
          <CardContent>
            <TopSkillsChart data={skills} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
