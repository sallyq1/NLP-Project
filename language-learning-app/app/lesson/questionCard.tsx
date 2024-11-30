'use client'

import React, { useEffect, useState } from 'react'
import { Button } from "../../components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "../../components/ui/card"
import { Input } from "../../components/ui/input"
import { Label } from "../../components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select"
import axios from 'axios'
import { createClient } from '../../utils/supabase/client'

// initialize supabase client side client
const supabase = createClient()

export function QuestionCard(props: any) {
    const [HasChoices, setHasChoices] = useState(false)
    const [answer, setAnswer] = useState('')
    const [isCorrect, setisCorrect] = useState<boolean | null>(null)

    const [user, setUser] = useState<any>(null)

    // Get user data on mount
    useEffect(() => {
        const getUser = async () => {
            const { data, error } = await supabase.auth.getSession()
            if (error) throw error

            // if no user, then redirect to the login page
            if (data?.session?.user) {
                setUser(data.session.user)
            } else {
                window.location.href = '/login'
            }
        }
        
        getUser()

    }, [])

    useEffect(() => {
        // clear the answer whenever the question ID changes
        setAnswer('');
        setisCorrect(null); // reset is correct state
    }, [props.id]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault() // prevent form from reloading the page

        try {
            if (!user) {
                console.log('User is not logged in.')
                return
            }
            
            const response = await axios.post(
                `http://localhost:8000/lessons/attempt?user_answer=${answer}&question_id=${props.id}&user_id=${user.id}`,
            )

            setisCorrect(response.data.is_correct)
            
        }
        catch (error) {
          console.error('Error verifying the answer: ', error);
        }
    }

    return (
      <Card className="w-[750px] space-x-2 space-y-2 p-2">
        <CardHeader>
          <CardTitle className='font-semibold text-xl'>{props.questionType}</CardTitle>
          <CardDescription className='text-2xl'>{props.question}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
                {HasChoices ? (
                    <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="choices">Answer Choices</Label>
                        <Select>
                        <SelectTrigger id="choices">
                            <SelectValue placeholder="Select an answer choice" />
                        </SelectTrigger>
                        <SelectContent position="popper">
                            <SelectItem value="next">Next.js</SelectItem>
                            <SelectItem value="sveltekit">SvelteKit</SelectItem>
                            <SelectItem value="astro">Astro</SelectItem>
                            <SelectItem value="nuxt">Nuxt.js</SelectItem>
                        </SelectContent>
                        </Select>
                    </div>
                ) : (
                    <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="answer">Enter your answer here</Label>
                        <Input 
                            id="answer" 
                            placeholder="Your Answer" 
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                        />
                    </div>
                )}

            </div>
            <CardFooter className="flex justify-center">
                <Button type='submit'>Submit Answer</Button>
            </CardFooter>
          </form>
          {isCorrect != null && (
                    <div className="mt-4 text-center">
                        {isCorrect ? (
                            <p className="text-green-500 font-bold">Correct Answer!</p>
                        ) : (
                            <p className="text-red-500 font-bold">Incorrect Answer.</p>
                        )}
                    </div>
                )}
        </CardContent>
      </Card>
    )
}
  