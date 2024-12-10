export type Course = {
  code: string;
  description: string;
};

export type User = {
  id: string;
  name: string;
  username: string;
  coursesIds: string[];
};

export type Job = {
  title: string;
  link: string;
};
