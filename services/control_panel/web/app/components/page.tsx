import { ComponentsView } from "@/components/components-view";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Components — Control Panel" };

export default async function ComponentsPage() {
  const data = await api.features();
  return <ComponentsView features={data.features} />;
}
