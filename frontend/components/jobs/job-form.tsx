"use client";
import * as React from "react";
import { Loader2, Save } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import type { Job } from "@/lib/types";

interface Props {
  onCreated?: (job: Job) => void;
}

export function JobForm({ onCreated }: Props) {
  const [title, setTitle] = React.useState("");
  const [company, setCompany] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [skills, setSkills] = React.useState("");
  const [minYears, setMinYears] = React.useState<number>(0);
  const [education, setEducation] = React.useState("");
  const [busy, setBusy] = React.useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) {
      toast.error("Title and description are required.");
      return;
    }
    setBusy(true);
    try {
      const job = await api.createJob({
        title: title.trim(),
        company: company.trim(),
        description: description.trim(),
        required_skills: skills
          .split(",")
          .map((s) => s.trim().toLowerCase())
          .filter(Boolean),
        min_experience_years: Number(minYears) || 0,
        education_level: education,
      });
      toast.success(`Created job: ${job.title}`);
      onCreated?.(job);
      setTitle("");
      setCompany("");
      setDescription("");
      setSkills("");
      setMinYears(0);
      setEducation("");
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Job Description</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={submit} className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2 md:col-span-1">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Senior Backend Engineer"
            />
          </div>
          <div className="space-y-2 md:col-span-1">
            <Label htmlFor="company">Company</Label>
            <Input
              id="company"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="Acme Corp"
            />
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="desc">Job description *</Label>
            <Textarea
              id="desc"
              rows={8}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Paste the full job description here..."
            />
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="skills">
              Required skills (comma separated, optional — auto-extracted if empty)
            </Label>
            <Input
              id="skills"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="python, fastapi, postgresql, docker, kubernetes, aws"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="minyears">Minimum years of experience</Label>
            <Input
              id="minyears"
              type="number"
              min={0}
              step={0.5}
              value={minYears}
              onChange={(e) => setMinYears(Number(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="edu">Education level</Label>
            <select
              id="edu"
              value={education}
              onChange={(e) => setEducation(e.target.value)}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
            >
              <option value="">Any</option>
              <option value="school">High school</option>
              <option value="diploma">Diploma</option>
              <option value="bachelors">Bachelor's</option>
              <option value="masters">Master's</option>
              <option value="phd">PhD</option>
            </select>
          </div>
          <div className="md:col-span-2 flex justify-end">
            <Button type="submit" disabled={busy}>
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
              {busy ? "Saving..." : "Save job"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
