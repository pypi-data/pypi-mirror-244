## tlb32 - Tool for automatic calculation of operation codes in TL-B schemes.

### Example of use

0. install tlb32 with `pip install tlb32`

1. write `// request` or `// response` comment before message scheme
    ```
    // request
    transfer_notification query_id:uint64 amount:(VarUInteger 16)
                          sender:MsgAddress forward_payload:(Either Cell ^Cell)
                          = InternalMsgBody;
    ```

2. run `tlb32 <scheme_file>`

3. view result :)
    ```
    // request
    transfer_notification#736ad09c query_id:uint64 amount:(VarUInteger 16)
                          sender:MsgAddress forward_payload:(Either Cell ^Cell)
                          = InternalMsgBody;
    ```