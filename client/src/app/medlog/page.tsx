import Journal from "@/components/medlog/JournalClient";

export default async function MedLog() {
    const today = new Date().toISOString().split("T")[0];
    return <Journal className="px-4" today={today}></Journal>;
}
