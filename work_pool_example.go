// generated by chatGPT
package main

import (
    "fmt"
    "sync"
)

func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Printf("Worker %d started job %d\n", id, j)
        results <- j * 2
        fmt.Printf("Worker %d finished job %d\n", id, j)
    }
}

func main() {
    const numJobs = 10
    jobs := make(chan int, numJobs)
    results := make(chan int, numJobs)

    // Start workers
    const numWorkers = 3
    var wg sync.WaitGroup
    for w := 1; w <= numWorkers; w++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            worker(id, jobs, results)
        }(w)
    }

    // Send jobs
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)

    // Wait for workers to finish and close results channel
    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect results
    for r := range results {
        fmt.Println(r)
    }
}
