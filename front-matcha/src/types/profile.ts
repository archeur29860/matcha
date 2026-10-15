export interface ProfileCard {
  user_id: string
  username: string
  age: number
  location: string
  online: boolean
  tags: Tag[]
  bio: string
  image: string
  popularity: number
}

export interface Tag {
  id: string
  label: string
}