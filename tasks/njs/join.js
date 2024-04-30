var flag = "CSCG{This_is_a_fake_flag!}";

// Combines several responses asynchronously into a singel reply
async function join(r) {
    if (r.method !== "POST") {
        r.return(401, "Unsupported method\n");
        return;
    }

    let body  = JSON.parse((r.requestText));

    if (!body['endpoints']) {
        r.return(400, "Missing Parameters!");
        return;
    }

    // Make sure to prevent LFI since directory root does not apply to subrequests...
    let subs = body.endpoints.filter(sub => (typeof sub === "string" && !sub.includes(".")));
    if (subs.length === 0) {
        r.return(400, "No valid endpoint supplied!");
        return;
    }

    let response = await join_subrequests(r, subs);

    var ascii_error = "Error: No ASCII data!";
    
    // Using alloc() instead of allocUnsafe() to ensure no sensitive data is leaked!
    let reply_buffer = Buffer.alloc(response.length);

    if ( r.headersIn["Accept"] === "text/html; charset=utf-8" ) {
        // Remove non ASCII character
        let ascii_string = response.replace(/[^\x00-\x7F]/g, "");

        if ( ascii_string.length == 0 ) {
            // Joined response does not contain any ASCII data...
            reply_buffer.write(ascii_error);
        } else {
            reply_buffer.write(ascii_string);
        }

        // Return response as string
        r.return(200, reply_buffer.toString());
    } else {
        reply_buffer.write(response);

        // Return response as buffer
        r.return(200, reply_buffer);
    }
}

async function join_subrequests(r, subs) {

    let results = await Promise.all(subs.map(uri => r.subrequest("/data/" + uri)));
    let response = results.map(reply => (reply.responseText)).join("");

    return response;
}

export default { join };
