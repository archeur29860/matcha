export interface Location {
  street: string | null
  district: string | null
  city: string
  postcode: string
  department: string
}

export interface ProfileCard {
  user_id: string
  username: string
  age: number
  location: Location | null
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

export interface Picture {
	id: number
	url: string
}