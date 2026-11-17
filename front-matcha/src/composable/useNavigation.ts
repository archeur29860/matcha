import router from '@/router'

export function handleClickOnProfile(user_id: string) {
  // console.log('Click on profile', user_id)
  router.push(`/profile/${user_id}/`)
  
}