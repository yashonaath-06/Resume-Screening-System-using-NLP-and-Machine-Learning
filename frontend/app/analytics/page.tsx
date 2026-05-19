"use client";
import * as React from "react";
import { toast } from "sonner";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScoreDistributionChart } from "@/components/dashboard/score-distribution-chart";
import { TopSkillsChart } from "@/components/dashboard/top-skills-chart";
import { api } from "@/lib/api";
import type { ScoreBucket, SkillCount } from "@/lib/types";

export default function AnalyticsPage() {
  const [dist, setDist] = React.useState<ScoreBucket[]>([]);
  const [skills, setSkills] = React.useState<SkillCount[]>([]);

  React.useEffect(() => {
    (async () => {
      try {
        const [d, t] = await Promise.all([api.scoreDist(), api.topSkills(20)]);
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
        <h1 className="text-2xl font-bold tracking-tight">Analytics</h1>
        <p className="text-sm text-muted-foreground">
          Recruiter-grade insights from your resume pool.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>ATS score distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ScoreDistributionChart data={dist} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Top skills (resume pool)</CardTitle>
          </CardHeader>
          <CardContent>
            <TopSkillsChart data={skills} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
