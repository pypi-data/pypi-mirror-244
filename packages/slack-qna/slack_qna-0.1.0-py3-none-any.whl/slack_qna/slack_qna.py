import traceback
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from datetime import datetime
from slack_qna.schema import IncomingMessage, OutgoingMessage, Reactions, CommandHook

class SlackQna:

    def __init__(self, slack_bot_token, slack_app_token, bot_user_id, reactions=None):
        self.client = WebClient(token=slack_bot_token)
        self.socket_mode_client = SocketModeClient(app_token=slack_app_token)
        self.bot_user_id = bot_user_id
        self.reactions = reactions or Reactions(
            loading="thinking_face",
            success="white_check_mark",
            failed="x"
        )

    def register_handler(self, command_hook: CommandHook):
        self.command_hook = command_hook

    def post_message(self, outgoing_message: OutgoingMessage):
        
        if outgoing_message.data_type == "text" and isinstance(outgoing_message.data, str):
            self.client.chat_postMessage(
                channel=outgoing_message.channel_id,
                thread_ts=outgoing_message.thread_id,
                text=outgoing_message.data
            )
        elif outgoing_message.data_type == "image" and isinstance(outgoing_message.data, bytes):
            self.client.files_upload_v2(
                channel=outgoing_message.channel_id,
                thread_ts=outgoing_message.thread_id,
                file=outgoing_message.data,
                filename='data.png'
            )
        elif outgoing_message.data_type == "file" and isinstance(outgoing_message.data, bytes):
            self.client.files_upload_v2(
                channel=outgoing_message.channel_id,
                thread_ts=outgoing_message.thread_id,
                file=outgoing_message.data,
                filename='data.txt'
            )
            

    def process_message(self, incoming_message: IncomingMessage):
        print(f"[{datetime.now().isoformat()}] SLACK_PROCESS_MESSAGE: {incoming_message}")
        
        if self.command_hook is None:
            return
        
        if self.reactions.loading is not None:
            reaction = self.client.reactions_add(
                channel=incoming_message.channel_id,
                name=self.reactions.loading,
                timestamp=incoming_message.message_id
            )
        
        try:
            
            if self.command_hook.is_sync:
                message = self.command_hook.handler(incoming_message)
                if message:
                    self.post_message(OutgoingMessage(
                        data_type=self.command_hook.data_type,
                        channel_id=incoming_message.channel_id,
                        thread_id=incoming_message.message_id,
                        data=message
                    ))
                if self.reactions.success is not None:
                    self.client.reactions_add(
                        channel=incoming_message.channel_id,
                        name=self.reactions.success,
                        timestamp=incoming_message.message_id
                    )
            else:
                self.command_hook.handler(incoming_message)
        except Exception as e:
            print(e)
            if self.reactions.failed is not None:
                self.client.reactions_add(
                    channel=incoming_message.channel_id,
                    name=self.reactions.failed,
                    timestamp=incoming_message.message_id
                )
            self.post_message(OutgoingMessage(
                data_type="text",
                channel_id=incoming_message.channel_id,
                thread_id=incoming_message.message_id,
                data=f"Sorry, something went wrong.\n{str(e)}"
            ))
        finally:
            if self.reactions.loading is not None:
                self.client.reactions_remove(
                    channel=incoming_message.channel_id,
                    name=self.reactions.loading,
                    timestamp=incoming_message.message_id
                )

    def listen(self, command=None, mention=None, direct_message=None):
        
        def process_request(client: SocketModeClient, req: SocketModeRequest):
            client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
            try:
                if req.type == "events_api":
                    event = req.payload.get("event", {})
                    print(f"[{datetime.now().isoformat()}] SLACK_PROCESS_REQUEST: {event}")

                    if event.get("user") != self.bot_user_id and event.get("type") == "message":
                        
                        user_id_tag = f"<@{self.bot_user_id}>"
                        message: str = event.get("text")
                        if message.startswith(user_id_tag):
                            message = message.replace(user_id_tag, "").strip()
                        
                        self.process_message(IncomingMessage(
                            message_id=event.get("ts"),
                            channel_id=event.get("channel"),
                            raw=event.get("text"),
                            message=message,
                            thread_id=event.get("thread_ts")
                        ))
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                print(e)
                print(traceback.format_exc())
            
                    
        self.socket_mode_client.socket_mode_request_listeners.append(process_request)
        self.socket_mode_client.connect()
        
        print(f"[{datetime.now().isoformat()}] SLACK_START_LISTENING: {command, mention, direct_message}")
        from threading import Event
        Event().wait()
