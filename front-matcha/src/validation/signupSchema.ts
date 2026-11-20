import { z } from 'zod'
import { toTypedSchema } from '@vee-validate/zod'

export const signupSchema = toTypedSchema(z.object({
    email: z.string().trim().email().max(255),
    username: z.string().trim().min(1, 'username must be at least 1 characters.')
    .max(50, 'must username be at most 50 characters.'),
    first_name: z.string().trim()
    .min(2, 'username must be at least 2 characters.')
    .max(50, 'must username be at most 50 characters.'),
    last_name: z.string().trim()
    .min(2, 'username must be at least 2 characters.')
    .max(50, 'must username be at most 50 characters.'),
    
    password: z.string()
    .min(8, 'password must be at least 8 characters.')
    .max(255, 'password must be at most 255 characters.'),
    
    pwd: z.string().min(1),
    }).refine((v) => v.password === v.pwd, {
    message: "must be similar",
    path: ['pwd'],
    }))
