"use client";
import * as React from "react";
import { useParams } from "next/navigation";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

import { ReportView } from "@/components/reports/report-view";
import { api } from "@/lib/api";
import type { ScreeningReport } from "@/lib/types";

export default function ReportPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params?.id);
  const [data, setData] = React.useState<ScreeningReport | null>(null);

  React.useEffect(() => {
    if (!Number.isFinite(id)) return;
    (async () => {
      try {
        setData(await api.report(id));
      } catch (e) {
        toast.error((e as Error).message);
      }
    })();
  }, [id]);

  if (!data) {
    return (
      <div className="flex items-center gap-2 text-muted-foreground">
        <Loader2 className="h-4 w-4 animate-spin" />
        Loading report...
      </div>
    );
  }

  return <ReportView data={data} />;
}
