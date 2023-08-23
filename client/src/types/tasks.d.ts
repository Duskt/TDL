export interface TaskClass {
    class_id: number,
    repeat_next: Date,
    repeat_mode: null | "never",
    last_modified: Date,
    title: string,
    description: string,
}

export interface TaskInstance {
    instance_id: number,
    class_id: number,
    date: Date,
    done: boolean,
}