export enum AppealStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  REJECTED = 'rejected',
  CLOSED = 'closed',
}

export enum AppealCategory {
  ROADS = 'roads',
  LIGHTING = 'lighting',
  IMPROVEMENT = 'improvement',
  ECOLOGY = 'ecology',
  SAFETY = 'safety',
  HEALTHCARE = 'healthcare',
  UTILITIES = 'utilities',
  SOCIAL = 'social',
  OTHER = 'other',
}

export enum AppealPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface User {
  id: number
  email: string
  full_name: string
  phone?: string
  role: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

export interface Appeal {
  id: number
  title: string
  description: string
  category: AppealCategory
  status: AppealStatus
  priority: AppealPriority
  latitude?: number
  longitude?: number
  address?: string
  district?: string
  images: string[]
  ai_summary?: string
  ai_sentiment?: string
  user_id: number
  department_id?: number
  created_at: string
  updated_at?: string
  resolved_at?: string
}

export interface AppealCreate {
  title: string
  description: string
  category?: AppealCategory
  latitude?: number
  longitude?: number
  address?: string
  images?: string[]
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
  phone?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

