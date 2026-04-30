import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const modules = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/modules" }),
  schema: z.object({
    title: z.string(),
    moduleNumber: z.number(),
    order: z.number(),
  }),
});

export const collections = { modules };
