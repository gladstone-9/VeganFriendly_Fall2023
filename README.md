# Restaurant Description Generator

A Prompt Engineering tool for automating text generation.

![alt text](https://github.com/gladstone-9/VeganFriendly_Fall2023/blob/main/Workflow_VeganFriendlyAutomation.png?raw=true)

This project interfaces with the [hugging chat API](https://github.com/Soulter/hugging-chat-api). A hugging chat account is required (modify hf.env credentials).



| Pros                   | Cons                      |
|:------------------------|:---------------------------|
| Free Model (meta-llama/Llama-2-70b-chat-hf) hosted on Hugging Chat Platform  | Model not trained for specific use                   |
| Free API                                                                     | Occasional overquerying block on account             |
| Easy to use, setup, and switch out, APIs                                     | Not currently directly interfaced with Monday.com    | 
| Customizable                                                                 | Currently handles specific formatting of Excel Files |

### Customizing Prompt
Edit both .txt files directly to customize.
- **template.txt** sets the system prompt. System prompts allow developers to prescribe the AI's style and task within certain bounds, making it more customizable and adaptable.
- **rules.txt** are prompts given to the model to refine the original output. Rules can be added or removed.
- **get_background()** creates the original prompt. Edit this function based on data available and purpose.
