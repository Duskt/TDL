export interface MoodDesc {
    body: string;
    date: string;
}

export type MoodDescGETReq = {
    date: string;
};

export type MoodDescGETRes = {
    body?: string;
};
