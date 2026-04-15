from agent import create_search_agent, create_scrape_agent, writer_chain , critic_chain

def run_research_pipeline(topic : str) -> dict:

    state = {}

    print("\n"+"="*50)
    print("step 1: search agent is working ")
    print("="*50)

    search_agrnt = create_search_agent()
    search_results = search_agrnt.invoke({
        "messages": [("user", f"Search the web for recent and relevant information on the topic: {topic}")]
    })

    state['search_results'] = search_results['messages'][-1].content


    print("\n"+" ="*50)


    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = create_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])


    print("\n"+"="*50)
    print("step 3 - Writer agent is compiling the research report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)


   