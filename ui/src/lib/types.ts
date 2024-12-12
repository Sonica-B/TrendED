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
  skills: string[];
};

export type Job = {
  title: string;
  description: string;
  employer: string;
  location: string;
  url: string;
};
