export type Course = {
  code: string;
  description: string;
  title: string;
  department: string;
};

export type User = {
  id: string;
  name: string;
  username: string;
  courseIds: string[];
};

export type Job = {
  title: string;
  link: string;
};
